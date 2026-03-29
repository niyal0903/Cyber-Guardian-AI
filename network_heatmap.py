"""
╔══════════════════════════════════════════════════════════╗
║      JARVIS — ANIMATED NETWORK HEATMAP                  ║
║  Router center, devices orbit, threats blink            ║
║  Pure matplotlib — zero data, zero API                  ║
╚══════════════════════════════════════════════════════════╝

INSTALL:
    pip install matplotlib numpy

USAGE:
    from network_heatmap import show_network_heatmap
    show_network_heatmap(devices)   # scan ke baad call karo

MAIN.PY MEIN ADD KARO:
    from network_heatmap import show_network_heatmap

    elif "network map" in command or "show heatmap" in command:
        if last_devices:
            speak("Opening animated network heatmap sir")
            show_network_heatmap(last_devices)
        else:
            speak("Sir please scan network first")
"""

import math
import time
import threading
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import socket
import requests

matplotlib.use("TkAgg")   # Windows ke liye best backend


# ─────────────────────────────────────────────
#  THREAT CLASSIFIER
# ─────────────────────────────────────────────

_SAFE_VENDORS = [
    "samsung", "apple", "xiaomi", "redmi", "oppo", "vivo", "realme",
    "oneplus", "intel", "dell", "hp", "hewlett", "lenovo", "asus",
    "acer", "google", "motorola", "nokia", "sony", "lg", "microsoft",
    "raspberry", "amazon",
]

_ROUTER_VENDORS = [
    "tp-link", "tplink", "d-link", "dlink", "netgear", "zyxel",
    "cisco", "jio", "reliance", "bsnl", "tenda", "huawei",
]

def _classify(vendor, name):
    """
    Returns: 'router', 'safe', 'suspicious', 'unknown'
    """
    v = (vendor or "").lower()
    n = (name   or "").lower()

    for r in _ROUTER_VENDORS:
        if r in v or r in n:
            return "router"

    for s in _SAFE_VENDORS:
        if s in v or s in n:
            return "safe"

    if "device-" in n or "unknown" in v or v == "":
        return "unknown"

    return "suspicious"


# ─────────────────────────────────────────────
#  TRAFFIC ESTIMATOR (ping based)
# ─────────────────────────────────────────────

def _estimate_traffic(ip):
    """Quick ping to estimate latency — lower = more active"""
    import subprocess
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "500", ip],
            capture_output=True, text=True, timeout=2
        )
        if "time=" in result.stdout:
            t = result.stdout.split("time=")[1].split("ms")[0].strip()
            return max(10, 100 - int(float(t)))  # Invert: low latency = high activity
    except:
        pass
    return 30  # Default medium traffic


# ─────────────────────────────────────────────
#  MAIN HEATMAP
# ─────────────────────────────────────────────

def show_network_heatmap(devices, speaker=None):
    """
    Main function — scan ke baad call karo.
    devices: list of (ip, mac, name, vendor)
    """

    if not devices:
        print("No devices to display.")
        return

    # ── Build device data ──
    device_data = []

    for ip, mac, name, vendor in devices:
        threat  = _classify(vendor, name)
        traffic = _estimate_traffic(ip)

        device_data.append({
            "ip"     : ip,
            "mac"    : mac,
            "name"   : name[:16],
            "vendor" : (vendor or "Unknown")[:20],
            "threat" : threat,
            "traffic": traffic,
        })

    # ── Separate routers from devices ──
    routers     = [d for d in device_data if d["threat"] == "router"]
    non_routers = [d for d in device_data if d["threat"] != "router"]

    if not non_routers and routers:
        non_routers = routers[1:]
        routers     = routers[:1]

    # ── Color map ──
    COLOR_MAP = {
        "safe"      : "#00FF88",   # Bright green
        "router"    : "#00AAFF",   # Blue
        "suspicious": "#FF6600",   # Orange
        "unknown"   : "#FF2244",   # Red
    }

    GLOW_MAP = {
        "safe"      : "#003322",
        "router"    : "#001133",
        "suspicious": "#331100",
        "unknown"   : "#330011",
    }

    # ── Figure setup ──
    fig = plt.figure(figsize=(14, 10), facecolor="#050510")
    ax  = fig.add_subplot(111, facecolor="#050510")

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.text(
        0.5, 0.97,
        "CYBER GUARDIAN — LIVE NETWORK MAP",
        ha="center", va="top",
        color="#00CCFF", fontsize=14, fontweight="bold",
        fontfamily="monospace"
    )

    local_ip = socket.gethostbyname(socket.gethostname())
    fig.text(
        0.5, 0.93,
        f"Your IP: {local_ip}   |   Devices: {len(devices)}   |   "
        f"Safe: {sum(1 for d in device_data if d['threat']=='safe')}   "
        f"Unknown: {sum(1 for d in device_data if d['threat']=='unknown')}",
        ha="center", va="top",
        color="#888888", fontsize=9, fontfamily="monospace"
    )

    # ── Legend ──
    legend_items = [
        (COLOR_MAP["safe"],       "Safe device"),
        (COLOR_MAP["router"],     "Router / AP"),
        (COLOR_MAP["suspicious"], "Suspicious"),
        (COLOR_MAP["unknown"],    "Unknown — threat"),
    ]
    for i, (col, label) in enumerate(legend_items):
        fig.text(
            0.02, 0.15 - i * 0.04,
            f"●  {label}",
            color=col, fontsize=9, fontfamily="monospace"
        )

    fig.text(
        0.02, 0.05,
        "Circle size = network activity\nBlink = potential threat",
        color="#555555", fontsize=8, fontfamily="monospace"
    )

    # ── Draw orbit rings ──
    n_rings = min(3, math.ceil(len(non_routers) / 4) + 1)
    for r_idx in range(1, n_rings + 1):
        ring = plt.Circle(
            (0, 0), r_idx * 1.6,
            fill=False,
            color="#111133",
            linewidth=0.5,
            linestyle="--",
        )
        ax.add_patch(ring)

    # ── Draw router at center ──
    router_name   = routers[0]["name"]   if routers else "Router"
    router_vendor = routers[0]["vendor"] if routers else ""

    router_circle = plt.Circle(
        (0, 0), 0.35,
        color="#00AAFF",
        zorder=5,
        alpha=0.9
    )
    ax.add_patch(router_circle)

    router_glow = plt.Circle(
        (0, 0), 0.5,
        color="#001144",
        zorder=4,
        alpha=0.5
    )
    ax.add_patch(router_glow)

    ax.text(
        0, -0.55, router_name,
        ha="center", va="top",
        color="#00AAFF", fontsize=8,
        fontfamily="monospace", fontweight="bold",
        zorder=6
    )

    # ── Draw orbit lines from router ──
    orbit_lines = []
    for d in non_routers:
        line, = ax.plot([], [], color="#111133", linewidth=0.5, zorder=1)
        orbit_lines.append(line)

    # ── Draw device circles ──
    device_circles = []
    device_glows   = []
    device_labels  = []
    device_ips     = []

    n = len(non_routers)
    for i, d in enumerate(non_routers):
        # Orbit ring assignment
        ring_num = (i % n_rings) + 1
        orbit_r  = ring_num * 1.6

        # Starting angle — evenly spaced
        angle_start = (2 * math.pi * i / max(n, 1))

        # Initial position
        x = orbit_r * math.cos(angle_start)
        y = orbit_r * math.sin(angle_start)

        # Circle size based on traffic
        size   = 0.12 + (d["traffic"] / 100) * 0.25
        color  = COLOR_MAP[d["threat"]]
        gcolor = GLOW_MAP[d["threat"]]

        # Glow circle
        glow = plt.Circle((x, y), size * 1.6, color=gcolor, zorder=2, alpha=0.4)
        ax.add_patch(glow)
        device_glows.append(glow)

        # Main circle
        circ = plt.Circle((x, y), size, color=color, zorder=3, alpha=0.9)
        ax.add_patch(circ)
        device_circles.append(circ)

        # Label
        lbl = ax.text(
            x, y - size - 0.15,
            d["name"],
            ha="center", va="top",
            color=color, fontsize=7,
            fontfamily="monospace",
            zorder=4
        )
        device_labels.append(lbl)

        # IP label
        ip_lbl = ax.text(
            x, y - size - 0.28,
            d["ip"],
            ha="center", va="top",
            color="#555555", fontsize=6,
            fontfamily="monospace",
            zorder=4
        )
        device_ips.append(ip_lbl)

    # ── Animation state ──
    frame_count = [0]

    # Orbit speeds — vary per device
    SPEEDS = [0.012 + (i % 5) * 0.004 for i in range(n)]

    # Starting angles
    angles = [(2 * math.pi * i / max(n, 1)) for i in range(n)]

    def animate(frame):
        frame_count[0] += 1
        t = frame_count[0]

        for i, d in enumerate(non_routers):
            ring_num = (i % n_rings) + 1
            orbit_r  = ring_num * 1.6

            # Update angle
            angles[i] += SPEEDS[i]
            x = orbit_r * math.cos(angles[i])
            y = orbit_r * math.sin(angles[i])

            size   = 0.12 + (d["traffic"] / 100) * 0.25
            color  = COLOR_MAP[d["threat"]]
            gcolor = GLOW_MAP[d["threat"]]

            # Update circle position
            device_circles[i].center = (x, y)
            device_glows[i].center   = (x, y)

            # Blink unknown/suspicious devices
            if d["threat"] in ("unknown", "suspicious"):
                blink_alpha = 0.5 + 0.5 * math.sin(t * 0.15)
                device_circles[i].set_alpha(blink_alpha)
                device_glows[i].set_alpha(blink_alpha * 0.4)

                # Pulse size
                pulse = size + 0.03 * math.sin(t * 0.2)
                device_circles[i].set_radius(pulse)
            else:
                # Gentle breathe for safe devices
                breathe = size + 0.01 * math.sin(t * 0.05 + i)
                device_circles[i].set_radius(breathe)

            # Update labels
            device_labels[i].set_position((x, y - size - 0.15))
            device_ips[i].set_position((x, y - size - 0.28))

            # Update orbit line router → device
            orbit_lines[i].set_data([0, x], [0, y])

        # Router glow pulse
        router_glow.set_radius(0.5 + 0.05 * math.sin(t * 0.08))

        return device_circles + device_glows + device_labels + device_ips + orbit_lines + [router_glow]

    ani = animation.FuncAnimation(
        fig,
        animate,
        interval=30,       # ~33 FPS
        blit=True,
        cache_frame_data=False,
    )

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
#  VOICE COMMAND INTEGRATION
# ─────────────────────────────────────────────
"""
main.py mein jarvis_loop ke andar yeh add karo:

    from network_heatmap import show_network_heatmap

    elif "network map" in command or "show heatmap" in command or "heatmap" in command:
        if last_devices:
            speak("Opening animated network heatmap sir")
            threading.Thread(
                target=show_network_heatmap,
                args=(last_devices,),
                daemon=True
            ).start()
        else:
            speak("Sir please scan network first then show heatmap")
"""


# ─────────────────────────────────────────────
#  STANDALONE TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Fake devices for testing
    test_devices = [
        ("192.168.1.1",   "14:CF:92:AA:BB:CC", "TPLink-Router",  "TP-Link"),
        ("192.168.1.2",   "E4:AB:89:11:22:33", "Samsung-2",      "Samsung"),
        ("192.168.1.3",   "B4:E6:2D:44:55:66", "Apple-3",        "Apple"),
        ("192.168.1.4",   "F4:60:E2:77:88:99", "Xiaomi-4",       "Xiaomi"),
        ("192.168.1.5",   "00:00:00:AA:BB:CC", "Device-5",       "Unknown"),
        ("192.168.1.6",   "AC:CF:85:DD:EE:FF", "Laptop-6",       "Intel"),
        ("192.168.1.7",   "00:11:22:33:44:55", "Device-7",       ""),
        ("192.168.1.8",   "7C:B0:C2:66:77:88", "Realme-8",       "Realme"),
    ]

    print("Jarvis Network Heatmap — Demo Mode")
    print("Close window to exit.\n")
    show_network_heatmap(test_devices)