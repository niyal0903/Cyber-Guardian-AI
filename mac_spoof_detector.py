import requests
import time


# ── Colors ───────────────────────────────────────────────────
class C:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    CYAN   = '\033[96m'
    BOLD   = '\033[1m'
    RESET  = '\033[0m'


# ── Known MAC Prefixes — RAM mein ────────────────────────────
# Pehle 6 chars = OUI = company
# Yeh RAM mein hain — file nahi!
KNOWN_VENDORS = {
    "8C:71:F8": "Samsung",
    "B8:27:EB": "Raspberry Pi",
    "00:50:56": "VMware",
    "08:00:27": "VirtualBox",
    "DC:A6:32": "Raspberry Pi",
    "3C:22:FB": "Apple",
    "A4:C3:F0": "Apple",
    "00:1A:11": "Google",
    "40:ED:98": "Samsung",
    "78:11:DC": "Samsung",
    "F8:8A:3C": "Intel",
    "00:0C:29": "VMware",
    "00:1C:42": "Parallels",
}


# ── Get Vendor from API ───────────────────────────────────────
def _get_vendor_api(mac):
    """
    MAC Vendor API se vendor fetch karo
    (tera existing get_vendor() jaisa)
    """
    try:
        url      = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text.strip()
        return "Unknown"
    except:
        return "Unknown"


def _get_mac_prefix_vendor(mac):
    """
    MAC ka pehla 3 bytes (OUI) check karo
    """
    prefix = mac.upper()[:8]   # "AA:BB:CC"
    return KNOWN_VENDORS.get(prefix, None)


# ── Main Detection Function ───────────────────────────────────
def check_mac_spoofing(devices, speaker=None, dash=None):
    """
    Scan ke baad sab devices check karo — MAC spoofing dhundo.

    cyberjarvis.py mein yeh call karo scan ke baad:
        from mac_spoof_detector import check_mac_spoofing
        check_mac_spoofing(devices, speaker, dash)

    Args:
        devices : list of (ip, mac, name, vendor) tuples
        speaker : win32com speaker (optional)
        dash    : dashboard object (optional)

    Returns:
        list — suspicious devices (RAM mein)
    """
    def speak(text):
        print(f"{C.CYAN}Jarvis: {text}{C.RESET}")
        if speaker:
            try:
                if dash: dash.set_mode("speaking")
                speaker.Speak(text)
                if dash: dash.set_mode("listening")
            except:
                pass

    print(f"\n{C.CYAN}{C.BOLD}[ MAC SPOOFING DETECTOR ]{C.RESET}")
    print(f"  Checking {len(devices)} devices... (RAM only)\n")

    # RAM mein suspicious list — file nahi!
    suspicious = []

    for ip, mac, name, vendor in devices:

        print(f"  Checking {ip} — {mac}...")

        # Method 1: OUI prefix check
        prefix_vendor = _get_mac_prefix_vendor(mac)

        # Method 2: API vendor check
        api_vendor    = _get_vendor_api(mac)
        time.sleep(0.5)   # API rate limit

        # ── Mismatch Logic ────────────────────────────────────

        # Check 1: Prefix vendor aur API vendor match karte hain?
        mismatch = False
        reason   = ""

        if prefix_vendor and api_vendor != "Unknown":
            if prefix_vendor.lower() not in api_vendor.lower() and \
               api_vendor.lower() not in prefix_vendor.lower():
                mismatch = True
                reason   = f"OUI says '{prefix_vendor}' but API says '{api_vendor}'"

        # Check 2: Random/locally administered MAC?
        # Second byte odd number = locally administered = possibly spoofed
        try:
            second_byte = int(mac.split(":")[0], 16)
            if second_byte & 0x02:   # LSB of first byte set = locally administered
                mismatch = True
                reason   = "Locally administered MAC — possibly randomized/spoofed"
        except:
            pass

        # Check 3: Known VM/VPN MAC patterns (often used for spoofing)
        vm_prefixes = ["00:0C:29", "00:50:56", "08:00:27", "00:1C:42"]
        mac_upper   = mac.upper()
        for vm_prefix in vm_prefixes:
            if mac_upper.startswith(vm_prefix):
                reason   = f"VM/Virtual MAC detected — {api_vendor}"
                # Not necessarily spoofing — just flag it
                print(f"  {C.YELLOW}[VM] {ip} — {mac} — {reason}{C.RESET}")

        # ── Alert ─────────────────────────────────────────────
        if mismatch:
            suspicious.append({
                "ip"            : ip,
                "mac"           : mac,
                "name"          : name,
                "claimed_vendor": prefix_vendor or "Unknown",
                "actual_vendor" : api_vendor,
                "reason"        : reason
            })

            print(f"\n  {C.RED}{C.BOLD}⚠ MAC SPOOFING SUSPECTED!{C.RESET}")
            print(f"  {C.RED}IP     : {ip}{C.RESET}")
            print(f"  {C.RED}MAC    : {mac}{C.RESET}")
            print(f"  {C.RED}Reason : {reason}{C.RESET}\n")

            speak(
                f"Sir! Possible MAC spoofing detected at IP {ip}. "
                f"Device MAC address does not match its vendor. "
                f"{reason}. This device may be hiding its real identity!"
            )

            if dash:
                dash.set_mode("alert")

        else:
            vendor_display = api_vendor if api_vendor != "Unknown" else (prefix_vendor or "Unknown")
            print(f"  {C.GREEN}✓ {ip} — {mac} — {vendor_display} — OK{C.RESET}")

    # ── Summary ───────────────────────────────────────────────
    print(f"\n  {'─'*42}")
    print(f"  Devices checked  : {len(devices)}")
    print(f"  Suspicious found : {C.RED if suspicious else C.GREEN}{len(suspicious)}{C.RESET}")

    if suspicious:
        speak(f"Sir, MAC spoofing check complete. Found {len(suspicious)} suspicious devices!")
        if dash:
            dash.set_mode("alert")
    else:
        speak("Sir, MAC spoofing check complete. All devices look legitimate!")
        print(f"  {C.GREEN}All devices clean!{C.RESET}")

    print(f"  {'─'*42}\n")

    return suspicious   # RAM mein return — file nahi!


# ── Standalone Test ───────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{C.CYAN}{C.BOLD}")
    print("╔══════════════════════════════════════╗")
    print("║  JARVIS — MAC Spoof Detector         ║")
    print("║  RAM Only — No Data Stored           ║")
    print("╚══════════════════════════════════════╝")
    print(C.RESET)

    # Test devices
    test_devices = [
        ("192.168.1.1",  "8C:71:F8:AA:BB:CC", "Router",  "Samsung"),
        ("192.168.1.5",  "B8:27:EB:11:22:33", "Unknown", "Unknown"),
        ("192.168.1.8",  "02:00:00:AA:BB:CC", "Unknown", "Unknown"),  # locally administered
        ("192.168.1.10", "00:0C:29:AA:BB:CC", "VM",      "VMware"),
    ]

    results = check_mac_spoofing(test_devices)

    if results:
        print(f"{C.RED}Suspicious devices:{C.RESET}")
        for d in results:
            print(f"  → {d['ip']} | {d['mac']} | {d['reason']}")
    else:
        print(f"{C.GREEN}No spoofing detected!{C.RESET}")