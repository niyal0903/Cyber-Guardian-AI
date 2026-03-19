import socket
import psutil
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

try:
    from scapy.all import ARP, Ether, srp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# ── Colors ────────────────────────────────────────────────────
class C:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    CYAN   = '\033[96m'
    WHITE  = '\033[97m'
    BOLD   = '\033[1m'
    RESET  = '\033[0m'


# ══════════════════════════════════════════════════════════════
class CyberAI:

    def __init__(self):
        print(f"\n{C.CYAN}{C.BOLD}")
        print("╔══════════════════════════════════════╗")
        print("║     CYBER AI MODULE  —  ONLINE       ║")
        print("║     J.A.R.V.I.S  v4.0               ║")
        print("╚══════════════════════════════════════╝")
        print(C.RESET)

    # ── 1. ANALYZE THREAT ─────────────────────────────────────
    def analyze_threat(self, devices):
        try:
            if not devices:
                return "LOW"

            total   = len(devices)
            unknown = 0
            flagged = []

            for device in devices:
                ip     = device[0] if len(device) > 0 else "?"
                vendor = device[3] if len(device) > 3 else "Unknown"

                vendor_lower = vendor.lower()
                is_known = any(brand in vendor_lower for brand in [
                    "samsung", "apple", "xiaomi", "oppo", "vivo",
                    "realme", "oneplus", "intel", "tp-link", "google",
                    "amazon", "microsoft", "dell", "hp", "lenovo"
                ])

                if not is_known or vendor in ("Unknown Vendor", "Unknown", ""):
                    unknown += 1
                    flagged.append(ip)

            if unknown == 0:
                level = "LOW"
            elif unknown <= 2:
                level = "MEDIUM"
            else:
                level = "HIGH"

            color = C.GREEN if level == "LOW" else (C.YELLOW if level == "MEDIUM" else C.RED)
            print(f"\n{C.BOLD}[ THREAT ANALYSIS ]{C.RESET}")
            print(f"  Total Devices  : {C.CYAN}{total}{C.RESET}")
            print(f"  Unknown        : {C.RED}{unknown}{C.RESET}")
            print(f"  Flagged IPs    : {C.RED}{', '.join(flagged) if flagged else 'None'}{C.RESET}")
            print(f"  Threat Level   : {color}{C.BOLD}{level}{C.RESET}\n")

            return level

        except Exception as e:
            print(f"analyze_threat error: {e}")
            return "MEDIUM"

    # ── 2. GET ADVICE ─────────────────────────────────────────
    def get_advice(self, threat_level):
        advice_map = {
            "LOW":    f"{C.GREEN}Network safe hai.{C.RESET} Sab devices pehchane hue hain.",
            "MEDIUM": f"{C.YELLOW}Caution!{C.RESET} Kuch unknown devices hain. Router logs check karo.",
            "HIGH":   f"{C.RED}ALERT! High threat!{C.RESET} Router password change karo!",
        }
        advice = advice_map.get(threat_level, "Unknown threat level.")
        print(f"\n{C.BOLD}[ AI ADVICE ]{C.RESET}")
        print(f"  {advice}\n")
        return advice

    # ── 3. FAST PORT SCAN ─────────────────────────────────────
    def port_scan(self, target, port_range=(1, 1025), max_workers=150):
        print(f"\n{C.BOLD}[ PORT SCAN ]{C.RESET}")
        print(f"  Target  : {C.CYAN}{target}{C.RESET}")
        print(f"  Scanning...\n")

        open_ports = []

        def check_one_port(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((target, port))
                s.close()
                return port if result == 0 else None
            except socket.error:
                return None

        try:
            ports = range(port_range[0], port_range[1])
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(check_one_port, p): p for p in ports}
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        open_ports.append(result)
                        service = self._get_service_name(result)
                        print(f"  {C.GREEN}[OPEN]{C.RESET} Port {C.CYAN}{result}{C.RESET} — {service}")

            open_ports.sort()

            if not open_ports:
                print(f"  {C.YELLOW}No open ports found.{C.RESET}")

            print(f"\n  Total open ports: {C.BOLD}{len(open_ports)}{C.RESET}\n")
            return open_ports

        except Exception as e:
            print(f"Port scan error: {e}")
            return []

    def _get_service_name(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 445: "SMB", 3306: "MySQL",
            3389: "RDP", 5900: "VNC", 8080: "HTTP-Alt",
        }
        return services.get(port, "Unknown Service")

    # ── 4. NETWORK SCAN ───────────────────────────────────────
    def scan_network(self, subnet=None):
        if not SCAPY_AVAILABLE:
            print("Scapy not installed!")
            return []

        try:
            if subnet is None:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                subnet   = ".".join(local_ip.split(".")[:3]) + ".0/24"

            print(f"\n{C.BOLD}[ NETWORK SCAN ]{C.RESET}")
            print(f"  Subnet  : {C.CYAN}{subnet}{C.RESET}")
            print(f"  Scanning...\n")

            arp    = ARP(pdst=subnet)
            ether  = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether / arp
            result = srp(packet, timeout=3, verbose=0)[0]

            devices = []
            for sent, received in result:
                ip  = received.psrc
                mac = received.hwsrc
                devices.append((ip, mac))
                print(f"  {C.GREEN}[FOUND]{C.RESET} IP: {C.CYAN}{ip:16}{C.RESET} MAC: {mac}")

            print(f"\n  Total devices: {C.BOLD}{len(devices)}{C.RESET}\n")
            return devices

        except PermissionError:
            print(f"{C.RED}Error: Admin/root privileges chahiye!{C.RESET}")
            return []
        except Exception as e:
            print(f"Network scan error: {e}")
            return []

    # ── 5. CPU USAGE ──────────────────────────────────────────
    def cpu_usage(self):
        try:
            usage = psutil.cpu_percent(interval=1)
            color = C.GREEN if usage < 60 else (C.YELLOW if usage < 85 else C.RED)
            print(f"  CPU Usage : {color}{usage}%{C.RESET}")
            return usage
        except Exception as e:
            print(f"CPU error: {e}")
            return 0

    # ── 6. RAM USAGE ──────────────────────────────────────────
    def ram_usage(self):
        try:
            mem   = psutil.virtual_memory()
            usage = mem.percent
            total = round(mem.total / (1024**3), 1)
            used  = round(mem.used  / (1024**3), 1)
            color = C.GREEN if usage < 60 else (C.YELLOW if usage < 85 else C.RED)
            print(f"  RAM Usage : {color}{usage}%{C.RESET} ({used}GB / {total}GB)")
            return usage
        except Exception as e:
            print(f"RAM error: {e}")
            return 0

    # ── 7. SYSTEM STATUS ──────────────────────────────────────
    def system_status(self):
        print(f"\n{C.BOLD}[ SYSTEM STATUS ]{C.RESET}")
        cpu = self.cpu_usage()
        ram = self.ram_usage()
        return {"cpu": cpu, "ram": ram}

    # ── 8. PUBLIC IP ──────────────────────────────────────────
    def ip_info(self):
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=5)
            ip = response.json()["ip"]

            try:
                geo     = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
                data    = geo.json()
                country = data.get("country_name", "Unknown")
                city    = data.get("city", "Unknown")
                isp     = data.get("org", "Unknown")

                print(f"\n{C.BOLD}[ IP INFO ]{C.RESET}")
                print(f"  Public IP : {C.CYAN}{ip}{C.RESET}")
                print(f"  Location  : {city}, {country}")
                print(f"  ISP       : {isp}\n")
                return {"ip": ip, "city": city, "country": country, "isp": isp}

            except:
                print(f"  Public IP : {C.CYAN}{ip}{C.RESET}")
                return {"ip": ip}

        except requests.ConnectionError:
            print(f"{C.RED}Error: Internet connection nahi hai!{C.RESET}")
            return None
        except requests.Timeout:
            print(f"{C.YELLOW}Error: Timeout.{C.RESET}")
            return None
        except Exception as e:
            print(f"IP info error: {e}")
            return None

    # ── 9. FULL REPORT ────────────────────────────────────────
    def full_report(self, devices):
        print(f"\n{C.CYAN}{C.BOLD}{'='*45}")
        print("   J.A.R.V.I.S  —  FULL SECURITY REPORT")
        print(f"   {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}")
        print(f"{'='*45}{C.RESET}\n")

        threat = self.analyze_threat(devices)
        self.get_advice(threat)
        self.system_status()
        self.ip_info()

        print(f"{C.CYAN}{'='*45}{C.RESET}\n")
        return threat