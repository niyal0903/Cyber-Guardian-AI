import requests
import webbrowser
import time
import folium
import os
from datetime import datetime
from collections import defaultdict

# ---------------- CONFIG ----------------
DDOS_THRESHOLD = 30
TIME_WINDOW    = 3
BLOCK_COOLDOWN = 60

# ---------------- STORAGE ----------------
packet_times = defaultdict(list)
tracked_ips  = {}
blocked_ips  = {}

# ---------------- LOCATION ----------------
def get_attack_location(ip):
    try:
        if ip in tracked_ips:
            return tracked_ips[ip]

        url = f"http://ip-api.com/json/{ip}"
        data = requests.get(url, timeout=5).json()

        if data.get("status") == "success":
            loc = {
                "ip": ip,
                "city": data.get("city"),
                "country": data.get("country"),
                "isp": data.get("isp"),
                "lat": data.get("lat"),
                "lon": data.get("lon"),
                "time": datetime.now().strftime("%H:%M:%S"),
            }
            tracked_ips[ip] = loc
            return loc
    except:
        return None

# ---------------- ATTACK LEVEL ----------------
def get_attack_level(count):
    if count > 100:
        return "HIGH"
    elif count > 60:
        return "MEDIUM"
    else:
        return "LOW"

# ---------------- BLOCK ----------------
def block_ip(ip):
    now = time.time()

    if ip in blocked_ips and now - blocked_ips[ip] < BLOCK_COOLDOWN:
        return

    print(f"🔥 Blocking IP: {ip}")
    os.system(f'netsh advfirewall firewall add rule name="BLOCK_{ip}" dir=in action=block remoteip={ip}')
    blocked_ips[ip] = now

# ---------------- MAP ----------------
def create_attack_map(locations):
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=4)

    for loc in locations:
        folium.CircleMarker(
            [loc["lat"], loc["lon"]],
            radius=8,
            popup=f"{loc['ip']} ({loc['city']})",
            color="red",
            fill=True
        ).add_to(m)

    m.save("attack_map.html")
    webbrowser.open("attack_map.html")

# ---------------- MAIN FUNCTION ----------------
def check_ddos(src_ip, speaker=None):
    now = time.time()

    # Time-based tracking
    packet_times[src_ip].append(now)

    # Old packets remove
    packet_times[src_ip] = [
        t for t in packet_times[src_ip]
        if now - t < TIME_WINDOW
    ]

    count = len(packet_times[src_ip])

    if count > DDOS_THRESHOLD:
        level = get_attack_level(count)

        print(f"\n⚠ DDoS ATTACK DETECTED!")
        print(f"IP: {src_ip}")
        print(f"Packets: {count} | Level: {level}")

        if speaker:
            speaker.Speak(f"Warning sir! {level} level DDoS attack detected")

        # Location
        loc = get_attack_location(src_ip)

        if loc:
            print(f"Location: {loc['city']}, {loc['country']}")

        # Map
        if loc:
            create_attack_map([loc])

        # Auto block
        block_ip(src_ip)

# ---------------- SHOW ATTACKERS ----------------
def show_all_attackers():
    print("\n🔥 ALL ATTACKERS")
    for ip, loc in tracked_ips.items():
        print(f"{ip} → {loc['city']}, {loc['country']}")

# ---------------- RESET ----------------
def reset():
    packet_times.clear()
    tracked_ips.clear()
    blocked_ips.clear()
    print("Reset complete")