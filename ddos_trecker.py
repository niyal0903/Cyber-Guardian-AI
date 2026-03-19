import requests
import webbrowser
from datetime import datetime
from collections import defaultdict

# ──────────────────────────────────────────────────────────────
#  DDoS Attack Location Tracker
#  Yeh module cyberjarvis.py mein import hoga
# ──────────────────────────────────────────────────────────────

# -------- Packet Counter --------
ddos_counter   = defaultdict(int)
tracked_ips    = {}   # ip → location info
blocked_ips    = set()

# DDoS threshold — kitne packets ke baad alert
DDOS_THRESHOLD = 50

# -------- IP Location Fetch --------
def get_attack_location(ip):
    """
    IP address ki real location fetch karo
    City, Country, ISP, lat/lon sab milega
    Free API — no key required
    """
    try:
        # Already tracked hai toh wahi return karo
        if ip in tracked_ips:
            return tracked_ips[ip]

        url      = f"http://ip-api.com/json/{ip}?fields=status,city,country,regionName,isp,lat,lon,org,as"
        response = requests.get(url, timeout=5)
        data     = response.json()

        if data.get("status") == "success":
            location = {
                "ip"      : ip,
                "city"    : data.get("city",       "Unknown"),
                "region"  : data.get("regionName", "Unknown"),
                "country" : data.get("country",    "Unknown"),
                "isp"     : data.get("isp",        "Unknown"),
                "org"     : data.get("org",        "Unknown"),
                "lat"     : data.get("lat"),
                "lon"     : data.get("lon"),
                "time"    : datetime.now().strftime("%H:%M:%S"),
            }
            tracked_ips[ip] = location
            return location
        else:
            return None

    except requests.ConnectionError:
        print("Location fetch failed: No internet")
        return None
    except Exception as e:
        print(f"Location fetch error: {e}")
        return None

# -------- Print Location Report --------
def print_location_report(location):
    """
    Location ka clean report print karo
    """
    if not location:
        print("Location not found")
        return

    print("\n" + "="*45)
    print("  🌍 DDOS ATTACKER LOCATION REPORT")
    print("="*45)
    print(f"  IP Address : {location['ip']}")
    print(f"  City       : {location['city']}")
    print(f"  Region     : {location['region']}")
    print(f"  Country    : {location['country']}")
    print(f"  ISP        : {location['isp']}")
    print(f"  Org        : {location['org']}")
    print(f"  Lat / Lon  : {location['lat']}, {location['lon']}")
    print(f"  Detected   : {location['time']}")
    print("="*45 + "\n")

# -------- Open Google Maps --------
def show_on_map(location):
    """
    Google Maps pe attacker ki location kholo
    """
    if not location:
        return

    lat = location.get("lat")
    lon = location.get("lon")

    if lat and lon:
        url = f"https://www.google.com/maps?q={lat},{lon}&z=12"
        print(f"Opening attack location on Google Maps...")
        print(f"Location: {location['city']}, {location['country']}")
        webbrowser.open(url)
    else:
        print("Map coordinates not available")

# -------- Block IP (Windows Firewall) --------
def block_attacker_ip(ip):
    """
    Windows Firewall se attacker IP block karo
    Admin privileges chahiye
    """
    import os

    if ip in blocked_ips:
        print(f"IP {ip} already blocked")
        return

    try:
        print(f"Blocking attacker IP: {ip}")
        os.system(
            f'netsh advfirewall firewall add rule '
            f'name="JARVIS_Block_{ip}" '
            f'dir=in action=block remoteip={ip}'
        )
        blocked_ips.add(ip)
        print(f"IP {ip} blocked successfully!")

    except Exception as e:
        print(f"Failed to block IP: {e}")

# -------- Main DDoS Check Function --------
def check_ddos(src_ip, speaker=None):
    """
    Har packet pe yeh function call karo
    Threshold cross karne pe:
    1. Location fetch karo
    2. Report print karo
    3. Map kholo
    4. IP block karo
    5. Jarvis bole (optional)

    Args:
        src_ip  : attacker IP
        speaker : win32com speaker object (optional, jarvis bolega)
    """
    ddos_counter[src_ip] += 1
    count = ddos_counter[src_ip]

    # Threshold cross hua
    if count == DDOS_THRESHOLD:
        print(f"\n⚠  DDOS ATTACK DETECTED!")
        print(f"   Attacker IP  : {src_ip}")
        print(f"   Packets Sent : {count}")

        # Jarvis bole
        if speaker:
            speaker.Speak(f"Warning sir! DDoS attack detected from {src_ip}")

        # Location track karo
        print("Tracking attacker location...")
        location = get_attack_location(src_ip)

        # Report print karo
        print_location_report(location)

        # Google Maps pe dikhao
        if location:
            show_on_map(location)

        # IP block karo
        block_attacker_ip(src_ip)

        # Jarvis final alert
        if speaker and location:
            city    = location.get("city",    "Unknown")
            country = location.get("country", "Unknown")
            speaker.Speak(
                f"Attacker located in {city}, {country} sir. "
                f"IP has been blocked."
            )

    # Har 100 packets pe update
    elif count > DDOS_THRESHOLD and count % 100 == 0:
        print(f"⚠  DDoS still ongoing from {src_ip} — {count} packets")

# -------- Show All Tracked Attackers --------
def show_all_attackers():
    """
    Abhi tak track kiye gaye sab attackers dikhao
    """
    if not tracked_ips:
        print("No attackers tracked yet")
        return

    print("\n" + "="*45)
    print("  ALL TRACKED ATTACKERS")
    print("="*45)
    for ip, loc in tracked_ips.items():
        status = "BLOCKED" if ip in blocked_ips else "ACTIVE"
        print(f"  [{status}] {ip} — {loc['city']}, {loc['country']}")
    print("="*45 + "\n")

# -------- Reset Counters --------
def reset_counters():
    """
    Sab counters reset karo — fresh start
    """
    ddos_counter.clear()
    tracked_ips.clear()
    blocked_ips.clear()
    print("DDoS counters reset")


# ──────────────────────────────────────────────────────────────
# TEST — seedha run karo check karne ke liye
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("DDoS Tracker Module — Test Mode")
    print("Testing location fetch for 8.8.8.8 (Google)...")

    loc = get_attack_location("8.8.8.8")
    print_location_report(loc)
    show_on_map(loc)