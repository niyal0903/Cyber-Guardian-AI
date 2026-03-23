import threading
import time
import logging
from collections import defaultdict
from datetime import datetime

# --------------- Logging Setup ---------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [EvilTwin] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("EvilTwin")

# --------------- Globals ---------------
_monitor_thread = None
_running        = False

# SSID → set of BSSIDs (MAC addresses)
ssid_bssid_map  = defaultdict(set)

# SSID → set of channels
ssid_channel_map = defaultdict(set)

# Already alerted SSIDs (avoid spam)
alerted_ssids   = set()

# Detected evil twins log
evil_twin_log   = []


# ─────────────────────────────────────────────
#  BEACON FRAME PARSER
# ─────────────────────────────────────────────
def _parse_beacon(packet):
    """
    Scapy se Beacon/Probe Response frame parse karo.
    Returns: (ssid, bssid, channel) or None
    """
    try:
        from scapy.all import Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeResp

        if not packet.haslayer(Dot11Beacon) and not packet.haslayer(Dot11ProbeResp):
            return None

        bssid = packet[Dot11].addr2
        if not bssid:
            return None

        # SSID extract
        ssid = ""
        channel = 0

        elt = packet[Dot11Elt]
        while elt:
            if elt.ID == 0:  # SSID element
                try:
                    ssid = elt.info.decode("utf-8", errors="ignore").strip()
                except:
                    ssid = ""
            elif elt.ID == 3:  # DS Parameter Set (channel)
                try:
                    channel = int.from_bytes(elt.info, "big")
                except:
                    channel = 0
            try:
                elt = elt.payload[Dot11Elt]
            except:
                break

        if not ssid:
            return None

        return ssid, bssid.upper(), channel

    except Exception as e:
        log.debug(f"Parse error: {e}")
        return None


# ─────────────────────────────────────────────
#  EVIL TWIN CHECK
# ─────────────────────────────────────────────
def _check_evil_twin(ssid, bssid, channel, speaker=None, dash=None):
    """
    Naya BSSID mila — evil twin conditions check karo:
    1. Same SSID pe 2+ different BSSIDs = Evil Twin
    2. Same SSID pe 2+ different channels = Suspicious
    """
    ssid_bssid_map[ssid].add(bssid)
    ssid_channel_map[ssid].add(channel)

    bssid_count   = len(ssid_bssid_map[ssid])
    channel_count = len(ssid_channel_map[ssid])

    # Evil Twin condition
    if bssid_count >= 2 and ssid not in alerted_ssids:
        alerted_ssids.add(ssid)

        bssid_list = list(ssid_bssid_map[ssid])
        channels   = list(ssid_channel_map[ssid])

        alert = {
            "time"     : datetime.now().strftime("%H:%M:%S"),
            "ssid"     : ssid,
            "bssids"   : bssid_list,
            "channels" : channels,
            "type"     : "EVIL TWIN" if bssid_count >= 2 else "SUSPICIOUS",
        }
        evil_twin_log.append(alert)

        # ── Console ──
        print("\n" + "═" * 55)
        print("  ⚠  EVIL TWIN ATTACK DETECTED!")
        print("═" * 55)
        print(f"  SSID     : {ssid}")
        print(f"  BSSIDs   : {', '.join(bssid_list)}")
        print(f"  Channels : {', '.join(map(str, channels))}")
        print(f"  Time     : {alert['time']}")
        print("═" * 55)
        print("  ACTION: Disconnect from this WiFi immediately!")
        print("=" * 55 + "\n")

        # ── Voice Alert ──
        if speaker:
            try:
                msg = (
                    f"Warning! Evil Twin attack detected on network {ssid}. "
                    f"There are {bssid_count} access points with the same name. "
                    f"This could be a Man in the Middle attack. Disconnect immediately sir."
                )
                speaker.Speak(msg)
            except Exception as e:
                log.error(f"Voice alert failed: {e}")

        # ── Dashboard ──
        if dash:
            try:
                dash.set_command(f"EVIL TWIN: {ssid} ({bssid_count} APs)")
            except:
                pass

        return True

    elif bssid_count >= 2:
        # Already alerted — just log silently
        log.info(f"[Known] Evil Twin still active: {ssid} ({bssid_count} BSSIDs)")

    return False


# ─────────────────────────────────────────────
#  PACKET HANDLER
# ─────────────────────────────────────────────
def _packet_handler(packet, speaker=None, dash=None):
    result = _parse_beacon(packet)
    if result:
        ssid, bssid, channel = result
        _check_evil_twin(ssid, bssid, channel, speaker, dash)


# ─────────────────────────────────────────────
#  MONITOR THREAD
# ─────────────────────────────────────────────
def _monitor_loop(iface, speaker, dash):
    """
    Background thread — WiFi beacon frames sniff karta hai.
    iface must be in MONITOR MODE.
    """
    global _running

    log.info(f"Starting Evil Twin monitor on interface: {iface}")
    log.info("Sniffing WiFi beacon frames... (monitor mode required)")

    try:
        from scapy.all import sniff

        while _running:
            sniff(
                iface=iface,
                prn=lambda pkt: _packet_handler(pkt, speaker, dash),
                count=50,          # 50 packets batch
                timeout=5,         # 5 sec timeout per batch
                store=False,
            )

    except PermissionError:
        log.error("Permission denied — run as Administrator/root")
        if speaker:
            speaker.Speak("Evil Twin monitor needs administrator privileges sir")

    except Exception as e:
        log.error(f"Sniffer error: {e}")
        if speaker:
            speaker.Speak(f"Evil Twin monitor error: {str(e)[:50]}")

    log.info("Evil Twin monitor stopped.")


# ─────────────────────────────────────────────
#  FALLBACK: Windows netsh scan (no monitor mode)
# ─────────────────────────────────────────────
def _windows_scan_loop(speaker, dash):
    """
    Windows pe monitor mode ke bina — netsh wlan show networks
    se visible SSIDs scan karo (limited but works without special hardware).
    """
    import subprocess

    global _running
    log.info("Using Windows netsh fallback (no monitor mode needed)")

    known_networks = {}  # ssid → {bssid: signal}

    while _running:
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "networks", "mode=bssid"],
                capture_output=True, text=True, timeout=10
            )

            lines = result.stdout.splitlines()
            current_ssid  = None
            current_bssid = None

            for line in lines:
                line = line.strip()

                if line.startswith("SSID") and "BSSID" not in line:
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        current_ssid = parts[1].strip()

                elif line.startswith("BSSID"):
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        # BSSID has colons — join remaining
                        current_bssid = parts[1].strip()
                        if current_ssid and current_bssid:
                            _check_evil_twin(
                                current_ssid,
                                current_bssid.upper(),
                                channel=0,
                                speaker=speaker,
                                dash=dash
                            )

        except Exception as e:
            log.error(f"netsh scan error: {e}")

        time.sleep(15)  # 15 seconds mein dobara scan


# ─────────────────────────────────────────────
#  PUBLIC API
# ─────────────────────────────────────────────
def start_evil_twin_monitor(speaker=None, dash=None, iface=None, use_windows=True):
  
    global _monitor_thread, _running, ssid_bssid_map, ssid_channel_map, alerted_ssids

    if _running:
        log.warning("Evil Twin monitor already running")
        if speaker:
            speaker.Speak("Evil Twin monitor is already running sir")
        return

    # Reset state
    ssid_bssid_map  = defaultdict(set)
    ssid_channel_map = defaultdict(set)
    alerted_ssids   = set()

    _running = True

    if use_windows or iface is None:
        # Windows netsh fallback
        target = _windows_scan_loop
        args   = (speaker, dash)
    else:
        # Scapy monitor mode
        target = _monitor_loop
        args   = (iface, speaker, dash)

    _monitor_thread = threading.Thread(
        target=target,
        args=args,
        daemon=True,
        name="EvilTwinMonitor"
    )
    _monitor_thread.start()

    msg = "Evil Twin attack monitor started sir. Scanning for duplicate access points."
    log.info(msg)
    if speaker:
        speaker.Speak(msg)
    if dash:
        try:
            dash.set_command("Evil Twin Monitor: ACTIVE")
        except:
            pass


def stop_evil_twin_monitor(speaker=None, dash=None):
    """Evil Twin monitor band karo."""
    global _running

    if not _running:
        log.warning("Monitor not running")
        return

    _running = False

    summary = get_evil_twin_summary()
    log.info(f"Monitor stopped. Total evil twins detected: {summary['total_detected']}")

    if speaker:
        n = summary["total_detected"]
        if n > 0:
            speaker.Speak(
                f"Evil Twin monitor stopped sir. {n} evil twin attacks were detected during this session."
            )
        else:
            speaker.Speak("Evil Twin monitor stopped. No evil twin attacks detected sir.")

    if dash:
        try:
            dash.set_command("Evil Twin Monitor: STOPPED")
        except:
            pass


def get_evil_twin_summary():
   
    return {
        "total_detected" : len(evil_twin_log),
        "events"         : evil_twin_log.copy(),
        "active_ssids"   : {
            ssid: list(bssids)
            for ssid, bssids in ssid_bssid_map.items()
            if len(bssids) >= 2
        },
    }


def show_evil_twin_report():
    """Console pe full report print karo."""
    summary = get_evil_twin_summary()

    print("\n" + "═" * 55)
    print("  EVIL TWIN DETECTION REPORT")
    print("═" * 55)
    print(f"  Total detections : {summary['total_detected']}")

    if summary["events"]:
        print("\n  Detected Events:")
        for i, ev in enumerate(summary["events"], 1):
            print(f"\n  [{i}] SSID     : {ev['ssid']}")
            print(f"       Time     : {ev['time']}")
            print(f"       BSSIDs   : {', '.join(ev['bssids'])}")
            print(f"       Channels : {', '.join(map(str, ev['channels']))}")
    else:
        print("\n  No evil twin attacks detected in this session.")

    print("═" * 55 + "\n")


# ─────────────────────────────────────────────
#  JARVIS COMMAND INTEGRATION
# ─────────────────────────────────────────────
"""
main.py mein yeh add karo jarvis_loop ke andar:

    elif "start evil twin" in command:
        speak("Starting Evil Twin attack monitor sir")
        start_evil_twin_monitor(speaker=speaker, dash=dash)

    elif "stop evil twin" in command:
        speak("Stopping Evil Twin monitor sir")
        stop_evil_twin_monitor(speaker=speaker, dash=dash)

    elif "evil twin report" in command:
        speak("Showing Evil Twin detection report sir")
        show_evil_twin_report()
"""


# ─────────────────────────────────────────────
#  STANDALONE TEST
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("Evil Twin Detector — Standalone Test")
    print("Simulating Evil Twin scenario...\n")

    # Simulate: 2 different BSSIDs with same SSID
    test_ssid = "HomeWiFi"
    _check_evil_twin(test_ssid, "AA:BB:CC:DD:EE:01", channel=6)
    time.sleep(0.5)
    _check_evil_twin(test_ssid, "FF:GG:HH:II:JJ:02", channel=11)

    show_evil_twin_report()