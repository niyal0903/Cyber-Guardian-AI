from scapy.all import sniff, Dot11, Dot11Deauth
import threading
import time


# ── Colors ───────────────────────────────────────────────────
class C:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    CYAN   = '\033[96m'
    BOLD   = '\033[1m'
    RESET  = '\033[0m'


# ── RAM mein sirf yeh store hoga (temporary) ─────────────────
_deauth_log   = []        # RAM mein — program band = gone
_attack_count = {}        # MAC: count — RAM mein
_monitoring   = False
_monitor_thread = None

ATTACK_THRESHOLD = 10     # 10+ packets = attack


# ── Packet Handler ────────────────────────────────────────────
def _packet_handler(packet, speaker=None, dash=None):
    """
    Har packet check karo — deauth hai toh count karo
    """
    # Deauth frame check — Type 0, Subtype 12
    if packet.haslayer(Dot11Deauth):

        attacker_mac = packet.addr2 or "Unknown"
        target_mac   = packet.addr1 or "Unknown"

        # RAM mein count karo
        if attacker_mac not in _attack_count:
            _attack_count[attacker_mac] = 0
        _attack_count[attacker_mac] += 1

        count = _attack_count[attacker_mac]

        print(f"{C.YELLOW}[DEAUTH] Packet from {attacker_mac} → {target_mac} (Count: {count}){C.RESET}")

        # ATTACK threshold cross hua?
        if count >= ATTACK_THRESHOLD:

            # Already alert diya? Spam mat karo
            already_alerted = any(
                log["mac"] == attacker_mac and log["alerted"]
                for log in _deauth_log
            )

            if not already_alerted:
                _trigger_alert(attacker_mac, target_mac, count, speaker, dash)

                # RAM mein log karo (file nahi!)
                _deauth_log.append({
                    "mac":     attacker_mac,
                    "target":  target_mac,
                    "count":   count,
                    "time":    time.strftime("%H:%M:%S"),
                    "alerted": True
                })


def _trigger_alert(attacker_mac, target_mac, count, speaker=None, dash=None):
    """
    Attack detect hua — alert karo
    """
    print(f"\n{C.RED}{C.BOLD}")
    print("╔══════════════════════════════════════════╗")
    print("║   ⚠  DEAUTH ATTACK DETECTED!             ║")
    print("╠══════════════════════════════════════════╣")
    print(f"║  Attacker MAC : {attacker_mac:<26}║")
    print(f"║  Target       : {target_mac:<26}║")
    print(f"║  Packets      : {str(count):<26}║")
    print(f"║  Time         : {time.strftime('%H:%M:%S'):<26}║")
    print("╚══════════════════════════════════════════╝")
    print(C.RESET)

    # Jarvis voice alert
    if speaker:
        try:
            if dash:
                dash.set_mode("speaking")
            speaker.Speak(
                f"Sir! WiFi deauthentication attack detected! "
                f"Attacker MAC address is {attacker_mac}. "
                f"Someone is trying to disconnect all devices from the network!"
            )
            if dash:
                dash.set_mode("alert")
        except:
            pass

    # Dashboard alert
    if dash:
        try:
            dash.set_mode("alert")
            dash.add_ddos(
                ip      = "WiFi Attacker",
                city    = "Local Network",
                country = attacker_mac,
                packets = count
            )
        except:
            pass


# ── Start Monitor ─────────────────────────────────────────────
def start_deauth_monitor(speaker=None, dash=None, interface=None):
    """
    Background mein deauth attack monitor karo.

    cyberjarvis.py mein call karo:
        from wifi_deauth_detector import start_deauth_monitor
        start_deauth_monitor(speaker, dash)

    Args:
        speaker   : win32com speaker (optional)
        dash      : dashboard object (optional)
        interface : WiFi interface name (optional — auto detect)
    """
    global _monitoring, _monitor_thread

    if _monitoring:
        print(f"{C.YELLOW}[DEAUTH] Already monitoring!{C.RESET}")
        return

    _monitoring = True
    _attack_count.clear()
    _deauth_log.clear()

    def _run():
        print(f"{C.CYAN}[DEAUTH] Starting WiFi Deauth Monitor...{C.RESET}")
        print(f"{C.CYAN}[DEAUTH] Threshold: {ATTACK_THRESHOLD} packets = ATTACK{C.RESET}")
        print(f"{C.CYAN}[DEAUTH] RAM only — no data stored{C.RESET}\n")

        try:
            # Interface auto detect ya manual
            sniff_args = {
                "prn"   : lambda pkt: _packet_handler(pkt, speaker, dash),
                "store" : False,        # RAM save nahi karo
                "stop_filter": lambda x: not _monitoring,
            }
            if interface:
                sniff_args["iface"] = interface

            sniff(**sniff_args)

        except Exception as e:
            print(f"{C.RED}[DEAUTH] Error: {e}{C.RESET}")
            print(f"{C.YELLOW}[DEAUTH] Note: Admin/root privileges needed!{C.RESET}")

    _monitor_thread = threading.Thread(target=_run, daemon=True)
    _monitor_thread.start()

    if speaker:
        try:
            if dash: dash.set_mode("speaking")
            speaker.Speak("WiFi deauth attack monitor started sir. I will alert you if any attack is detected.")
            if dash: dash.set_mode("listening")
        except:
            pass

    print(f"{C.GREEN}[DEAUTH] Monitor started in background!{C.RESET}")


def stop_deauth_monitor(speaker=None, dash=None):
    """
    Monitor band karo
    """
    global _monitoring
    _monitoring = False
    _attack_count.clear()
    _deauth_log.clear()

    print(f"{C.YELLOW}[DEAUTH] Monitor stopped. RAM cleared.{C.RESET}")

    if speaker:
        try:
            if dash: dash.set_mode("speaking")
            speaker.Speak("WiFi deauth monitor stopped sir.")
            if dash: dash.set_mode("listening")
        except:
            pass


def get_deauth_status():
    """
    Current status return karo — RAM se
    """
    return {
        "monitoring"   : _monitoring,
        "attacks_seen" : len(_deauth_log),
        "active_attackers": list(_attack_count.keys()),
        "log"          : _deauth_log[-5:] if _deauth_log else []
    }


# ── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{C.CYAN}{C.BOLD}")
    print("╔══════════════════════════════════════╗")
    print("║  JARVIS — WiFi Deauth Detector       ║")
    print("║  RAM Only — No Data Stored           ║")
    print("║  Press Ctrl+C to stop                ║")
    print("╚══════════════════════════════════════╝")
    print(C.RESET)
    print(f"{C.YELLOW}Note: Run as Administrator for best results!{C.RESET}\n")

    start_deauth_monitor()

    try:
        while True:
            time.sleep(5)
            status = get_deauth_status()
            print(f"{C.CYAN}[STATUS] Monitoring: {status['monitoring']} | Attacks: {status['attacks_seen']}{C.RESET}")
    except KeyboardInterrupt:
        stop_deauth_monitor()
        print(f"\n{C.GREEN}Monitor stopped!{C.RESET}")