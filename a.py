# import speech_recognition as sr
# import threading
# import pythoncom
# import win32com.client
# import socket
# import requests
# from scapy.all import ARP, Ether, srp, sniff
# from cyberai import CyberAI
# import psutil
# import networkx as nx
# import matplotlib.pyplot as plt
# from twilio.rest import Client
# import webbrowser
# import os
# import concurrent.futures
# from datetime import datetime
# import subprocess  # ← HUD ke liye add kiya

# # -------- Colors (Terminal mein rang) --------
# class C:
#     RED     = '\033[91m'
#     GREEN   = '\033[92m'
#     YELLOW  = '\033[93m'
#     CYAN    = '\033[96m'
#     MAGENTA = '\033[95m'
#     WHITE   = '\033[97m'
#     BOLD    = '\033[1m'
#     RESET   = '\033[0m'

# # -------- MAC Vendor Lookup --------
# def get_vendor(mac):
#     try:
#         url = f"https://api.macvendors.com/{mac}"
#         response = requests.get(url, timeout=3)
#         if response.status_code == 200:
#             return response.text.strip()
#         return "Unknown Vendor"
#     except:
#         return "Unknown Vendor"

# # -------- Device Brand Detection (improved) --------
# def detect_brand(vendor):
#     vendor = vendor.lower()
#     brands = {
#         "samsung":   ("📱 Samsung",        "Phone / TV"),
#         "apple":     ("🍎 Apple",           "iPhone / MacBook"),
#         "xiaomi":    ("📱 Xiaomi",          "Redmi / Mi Phone"),
#         "redmi":     ("📱 Xiaomi",          "Redmi Phone"),
#         "oppo":      ("📱 Oppo",            "Oppo Phone"),
#         "vivo":      ("📱 Vivo",            "Vivo Phone"),
#         "realme":    ("📱 Realme",          "Realme Phone"),
#         "oneplus":   ("📱 OnePlus",         "OnePlus Phone"),
#         "amazon":    ("🔊 Amazon",          "Alexa / Fire TV"),
#         "intel":     ("💻 Intel",           "Laptop / PC"),
#         "realtek":   ("💻 Realtek",         "PC / Laptop"),
#         "huawei":    ("📱 Huawei",          "Huawei Device"),
#         "tp-link":   ("📡 TP-Link",         "Router / Switch"),
#         "d-link":    ("📡 D-Link",          "Router / Switch"),
#         "netgear":   ("📡 Netgear",         "Router"),
#         "jio":       ("📡 JioFi",           "JioFi Device"),
#         "raspberry": ("🖥  Raspberry",      "Raspberry Pi"),
#         "espressif": ("🔌 Espressif",       "ESP8266 / ESP32"),
#         "google":    ("🏠 Google",          "Chromecast / Home"),
#         "hikvision": ("📷 Hikvision",       "CCTV Camera"),
#         "dahua":     ("📷 Dahua",           "CCTV Camera"),
#         "microsoft": ("💻 Microsoft",       "Windows Device"),
#         "hon hai":   ("📱 Foxconn",         "Phone / Device"),
#     }
#     for key, (brand, dtype) in brands.items():
#         if key in vendor:
#             return brand, dtype
#     return ("❓ Unknown", "Unknown Device")

# # ══════════════════════════════════════════════════
# # WiFi Scan with Beautiful Output
# # ══════════════════════════════════════════════════
# def scan_wifi_devices():
#     hostname = socket.gethostname()
#     local_ip = socket.gethostbyname(hostname)
#     parts    = local_ip.split(".")
#     subnet   = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"

#     print(f"\n{C.CYAN}{C.BOLD}")
#     print("╔══════════════════════════════════════════════════════════╗")
#     print("║            🔍  NETWORK SCAN STARTED                     ║")
#     print(f"║  Subnet : {subnet:<47}║")
#     print(f"║  My IP  : {local_ip:<47}║")
#     print("╚══════════════════════════════════════════════════════════╝")
#     print(f"{C.RESET}")

#     arp    = ARP(pdst=subnet)
#     ether  = Ether(dst="ff:ff:ff:ff:ff:ff")
#     packet = ether / arp
#     result = srp(packet, timeout=3, verbose=0)[0]

#     devices = []
#     num = 1

#     print(f"{C.BOLD}{C.CYAN}{'#':>3}  {'DEVICE':25} {'TYPE':20} {'IP ADDRESS':17} {'MAC ADDRESS':19} {'VENDOR'}{C.RESET}")
#     print(f"{C.CYAN}{'─'*3}  {'─'*25} {'─'*20} {'─'*17} {'─'*19} {'─'*20}{C.RESET}")

#     for sent, received in result:
#         ip  = received.psrc
#         mac = received.hwsrc

#         try:
#             name = socket.gethostbyaddr(ip)[0]
#         except:
#             name = "Unknown"

#         vendor        = get_vendor(mac)
#         brand, dtype  = detect_brand(vendor)

#         if brand == "❓ Unknown":
#             row_color = C.YELLOW
#         else:
#             row_color = C.GREEN

#         print(
#             f"{row_color}"
#             f"{num:>3}.  "
#             f"{brand:25} "
#             f"{dtype:20} "
#             f"{ip:17} "
#             f"{mac:19} "
#             f"{vendor[:20]}"
#             f"{C.RESET}"
#         )

#         devices.append((ip, mac, name, vendor))
#         num += 1

#     print(f"\n{C.CYAN}{'─'*70}{C.RESET}")
#     print(f"{C.BOLD}  Total Devices Found : {C.GREEN}{len(devices)}{C.RESET}")

#     unknown_count = sum(
#         1 for _, _, _, v in devices
#         if detect_brand(v)[0] == "❓ Unknown"
#     )
#     if unknown_count > 0:
#         print(f"  {C.YELLOW}⚠  Unknown Devices   : {unknown_count}  ← Investigate these!{C.RESET}")
#     else:
#         print(f"  {C.GREEN}✓  All devices identified{C.RESET}")

#     print(f"{C.CYAN}{'─'*70}{C.RESET}\n")

#     return devices

# # ══════════════════════════════════════════════════
# # ⚡ FAST PORT SCANNER — 150 threads, 10x faster
# # ══════════════════════════════════════════════════

# PORT_INFO = {
#     21:    ("FTP",           "DANGER",  "Cleartext login!"),
#     22:    ("SSH",           "SAFE",    "Encrypted remote access"),
#     23:    ("Telnet",        "DANGER",  "Cleartext — disable karo!"),
#     25:    ("SMTP",          "WARNING", "Email server"),
#     53:    ("DNS",           "WARNING", "DNS server"),
#     80:    ("HTTP",          "WARNING", "Unencrypted website"),
#     110:   ("POP3",          "WARNING", "Email protocol"),
#     135:   ("RPC",           "DANGER",  "Windows exploit target!"),
#     139:   ("NetBIOS",       "DANGER",  "Worm propagation risk!"),
#     143:   ("IMAP",          "WARNING", "Email protocol"),
#     443:   ("HTTPS",         "SAFE",    "Encrypted website"),
#     445:   ("SMB",           "DANGER",  "WannaCry target!"),
#     1433:  ("MSSQL",         "DANGER",  "Database exposed!"),
#     3306:  ("MySQL",         "DANGER",  "Database exposed!"),
#     3389:  ("RDP",           "DANGER",  "BlueKeep — brute force target!"),
#     4444:  ("Metasploit",    "DANGER",  "Reverse shell — HACKED?"),
#     5432:  ("PostgreSQL",    "DANGER",  "Database exposed!"),
#     5900:  ("VNC",           "DANGER",  "Weak auth — easily hacked!"),
#     6379:  ("Redis",         "DANGER",  "No auth — data theft!"),
#     8080:  ("HTTP-Alt",      "WARNING", "Alternative web port"),
#     8443:  ("HTTPS-Alt",     "SAFE",    "Alternative HTTPS"),
#     27017: ("MongoDB",       "DANGER",  "No auth by default!"),
#     9200:  ("Elasticsearch", "DANGER",  "Data fully exposed!"),
#     8888:  ("Jupyter",       "DANGER",  "Code execution exposed!"),
# }

# def _check_one_port(args):
#     ip, port = args
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.settimeout(0.5)
#         result = s.connect_ex((ip, port))
#         s.close()
#         return port if result == 0 else None
#     except:
#         return None

# def port_scan(ip):
#     start_time = datetime.now()

#     print(f"\n{C.CYAN}{C.BOLD}")
#     print(f"╔══════════════════════════════════════════════════╗")
#     print(f"║         ⚡ FAST PORT SCAN                        ║")
#     print(f"║  Target : {ip:<39}║")
#     print(f"╚══════════════════════════════════════════════════╝{C.RESET}")
#     print(f"{C.YELLOW}  Scanning 1-1024 ports... please wait...{C.RESET}")

#     all_ports  = list(range(1, 1025))
#     args       = [(ip, port) for port in all_ports]
#     open_ports = []

#     with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
#         results    = executor.map(_check_one_port, args)
#         open_ports = [p for p in results if p is not None]

#     open_ports.sort()
#     elapsed = (datetime.now() - start_time).total_seconds()

#     if not open_ports:
#         print(f"\n  {C.GREEN}✓ No open ports found — device is secure{C.RESET}")
#         print(f"  {C.CYAN}Scan completed in {elapsed:.1f}s{C.RESET}")
#         return []

#     print(f"\n  {C.BOLD}{'PORT':>6}  {'SERVICE':15} {'RISK':8}  {'INFO'}{C.RESET}")
#     print(f"  {'─'*6}  {'─'*15} {'─'*8}  {'─'*35}")

#     danger_ports  = []
#     warning_ports = []

#     for port in open_ports:
#         if port in PORT_INFO:
#             name, risk, info = PORT_INFO[port]
#         else:
#             name, risk, info = "Unknown", "WARNING", "Unknown service"

#         if risk == "DANGER":
#             color = C.RED + C.BOLD
#             icon  = "🚨"
#             danger_ports.append(port)
#         elif risk == "WARNING":
#             color = C.YELLOW
#             icon  = "⚠️ "
#             warning_ports.append(port)
#         else:
#             color = C.GREEN
#             icon  = "✅"

#         print(f"  {color}{port:>6}  {name:15} {icon} {risk:6}  {info[:35]}{C.RESET}")

#     print(f"\n  {C.CYAN}{'─'*60}{C.RESET}")
#     print(f"  {C.BOLD}⚡ Scan done in {elapsed:.1f}s  |  Open ports: {len(open_ports)}{C.RESET}")

#     if danger_ports:
#         print(f"  {C.RED}{C.BOLD}🚨 DANGEROUS PORTS: {danger_ports}{C.RESET}")
#         print(f"  {C.RED}   → Turant action lo!{C.RESET}")
#     if warning_ports:
#         print(f"  {C.YELLOW}⚠️  WARNING PORTS : {warning_ports}{C.RESET}")
#     if not danger_ports and not warning_ports:
#         print(f"  {C.GREEN}✓ Sab safe hai!{C.RESET}")

#     return open_ports

# # -------- Suspicious Traffic Detection --------
# traffic_counter = {}

# # -------- Hacker Location Finder --------
# def get_hacker_location(ip):
#     try:
#         url      = f"http://ip-api.com/json/{ip}"
#         response = requests.get(url).json()
#         city     = response.get("city", "Unknown")
#         country  = response.get("country", "Unknown")
#         isp      = response.get("isp", "Unknown")
#         lat      = response.get("lat")
#         lon      = response.get("lon")
#         print(f"\n{C.RED}🌍 Hacker Location")
#         print(f"  City   : {city}")
#         print(f"  Country: {country}")
#         print(f"  ISP    : {isp}{C.RESET}")
#         return lat, lon
#     except:
#         print("Location not found")
#         return None, None

# # -------- Attack Map --------
# def show_attack_map(lat, lon):
#     if lat and lon:
#         url = f"https://www.google.com/maps?q={lat},{lon}"
#         print("Opening attack location on Google Map...")
#         webbrowser.open(url)

# # -------- ARP Spoofing Detection --------
# arp_table = {}

# # -------- Auto IP Blocker --------
# def block_ip(ip):
#     try:
#         print(f"{C.RED}Blocking attacker IP: {ip}{C.RESET}")
#         os.system(f'netsh advfirewall firewall add rule name="Block_{ip}" dir=in action=block remoteip={ip}')
#         print("IP Blocked Successfully")
#     except:
#         print("Failed to block IP")

# # -------- DDoS Detection --------
# ddos_counter = {}

# # -------- Packet Sniffer --------
# def packet_callback(packet):

#     if packet.haslayer(ARP) and packet[ARP].op == 2:
#         ip  = packet[ARP].psrc
#         mac = packet[ARP].hwsrc
#         if ip in arp_table:
#             if arp_table[ip] != mac:
#                 print(f"{C.RED}⚠ ARP Spoofing Detected!")
#                 print(f"  IP      : {ip}")
#                 print(f"  Real MAC: {arp_table[ip]}")
#                 print(f"  Fake MAC: {mac}{C.RESET}")
#         else:
#             arp_table[ip] = mac

#     if packet.haslayer("IP"):
#         src = packet["IP"].src
#         dst = packet["IP"].dst
#         print(f"Packet: {src} -> {dst}")

#         traffic_counter[src] = traffic_counter.get(src, 0) + 1
#         if traffic_counter[src] > 20:
#             print(f"{C.YELLOW}⚠ Suspicious Traffic from {src}{C.RESET}")
#             lat, lon = get_hacker_location(src)
#             show_attack_map(lat, lon)

#         ddos_counter[src] = ddos_counter.get(src, 0) + 1
#         if ddos_counter[src] > 50:
#             print(f"{C.RED}⚠ DDoS Attack! IP: {src}  Packets: {ddos_counter[src]}{C.RESET}")
#             lat, lon = get_hacker_location(src)
#             show_attack_map(lat, lon)
#             block_ip(src)

# def start_sniffer():
#     print(f"\n{C.CYAN}Starting Packet Sniffer...{C.RESET}")
#     sniff(prn=packet_callback, count=10)

# # -------- Intrusion Detection --------
# known_devices = []

# def intrusion_detection(devices):
#     print(f"\n{C.CYAN}{C.BOLD}[Intrusion Detection]{C.RESET}")
#     for ip, mac, name, vendor in devices:
#         if mac not in known_devices:
#             brand, dtype = detect_brand(vendor)
#             print(f"  {C.YELLOW}⚠ Unknown Device  IP: {ip}  MAC: {mac}  Type: {brand}{C.RESET}")

# # -------- AI Threat Prediction --------
# def ai_threat_prediction(devices):
#     unknown = sum(1 for _, _, _, v in devices if detect_brand(v)[0] == "❓ Unknown")
#     score   = 0
#     if unknown > 2: score += 2
#     if len(devices) > 8: score += 1

#     threat = "High" if score >= 3 else "Medium" if score >= 1 else "Low"
#     color  = C.RED if threat == "High" else C.YELLOW if threat == "Medium" else C.GREEN
#     print(f"\n{color}{C.BOLD}AI Threat Level: {threat}{C.RESET}")
#     return threat

# # -------- Network Map --------
# def network_map(devices):
#     print(f"\n{C.CYAN}{C.BOLD}[Network Map]{C.RESET}")
#     unknown = 0
#     for ip, mac, name, vendor in devices:
#         brand, dtype = detect_brand(vendor)
#         color = C.YELLOW if brand == "❓ Unknown" else C.GREEN
#         print(f"  {color}{brand:25} IP: {ip}{C.RESET}")
#         if brand == "❓ Unknown":
#             unknown += 1

#     risk  = "High" if unknown > 2 else "Medium" if unknown > 0 else "Low"
#     color = C.RED if risk == "High" else C.YELLOW if risk == "Medium" else C.GREEN
#     print(f"\n  {color}Network Risk Level: {risk}{C.RESET}")
#     return risk

# # -------- Network Graph --------
# def network_graph(devices):
#     G      = nx.Graph()
#     router = "Router"
#     G.add_node(router)
#     for ip, mac, name, vendor in devices:
#         brand, _ = detect_brand(vendor)
#         label    = f"{brand}\n{ip}"
#         G.add_node(label)
#         G.add_edge(router, label)
#     pos = nx.spring_layout(G)
#     nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=8)
#     plt.title("Network Device Map")
#     plt.show()

# # -------- SOC Dashboard --------
# def soc_dashboard(devices, threat):
#     cpu   = psutil.cpu_percent()
#     ram   = psutil.virtual_memory().percent
#     color = C.RED if threat == "High" else C.YELLOW if threat == "Medium" else C.GREEN
#     print(f"\n{C.CYAN}{C.BOLD}╔══════════════════════════╗")
#     print(f"║   CYBER AI SOC DASHBOARD  ║")
#     print(f"╠══════════════════════════╣{C.RESET}")
#     print(f"  CPU Usage       : {cpu}%")
#     print(f"  RAM Usage       : {ram}%")
#     print(f"  Connected Devs  : {len(devices)}")
#     print(f"  Threat Level    : {color}{threat}{C.RESET}")
#     print(f"{C.CYAN}╚══════════════════════════╝{C.RESET}")

# # ══════════════════════════════════════════════════
# # ✅ IRON MAN HUD LAUNCHER
# # ══════════════════════════════════════════════════
# _hud_process = None

# def launch_hud():
#     global _hud_process
#     hud_file = os.path.join(
#         os.path.dirname(os.path.abspath(__file__)),
#         "jarvis_desktop_hud.py"
#     )
#     if not os.path.exists(hud_file):
#         print(f"{C.YELLOW}[HUD] jarvis_desktop_hud.py same folder mein nahi hai!{C.RESET}")
#         return
#     if _hud_process is not None and _hud_process.poll() is None:
#         print(f"{C.CYAN}[HUD] Already running!{C.RESET}")
#         return
#     print(f"{C.CYAN}[HUD] Launching Iron Man Dashboard...{C.RESET}")
#     _hud_process = subprocess.Popen(
#         ["python", hud_file],
#         creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0
#     )
#     print(f"{C.GREEN}[HUD] Iron Man Dashboard launched! ✓{C.RESET}")

# # ══════════════════════════════════════════════════
# # VOICE LOOP — Same as original + HUD command
# # ══════════════════════════════════════════════════
# def jarvis_loop():

#     pythoncom.CoInitialize()
#     speaker = win32com.client.Dispatch("SAPI.SpVoice")
#     cyber   = CyberAI()

#     def speak(text):
#         print(f"{C.MAGENTA}Jarvis: {text}{C.RESET}")
#         speaker.Speak(text)

#     recognizer = sr.Recognizer()
#     mic        = sr.Microphone()

#     with mic as source:
#         recognizer.adjust_for_ambient_noise(source, duration=1)

#     speak("Jarvis is online, tell me sir")

#     while True:
#         try:
#             with mic as source:
#                 print(f"\n{C.CYAN}Listening...{C.RESET}")
#                 audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

#             command = recognizer.recognize_google(audio, language="en-IN").lower().strip()
#             print(f"{C.WHITE}You said: {command}{C.RESET}")

#             if "system status" in command:
#                 speak("Checking system status")
#                 cyber.cpu_usage()
#                 cyber.ram_usage()

#             elif any(w in command for w in [
#                 "open hud", "iron man", "hud", "dashboard",
#                 "open dashboard", "show hud"
#             ]):
#                 speak("Opening Iron Man HUD Dashboard sir")
#                 threading.Thread(target=launch_hud, daemon=True).start()

#             elif "scan network" in command:
#                 speak("Scanning network devices, please wait sir")

#                 devices = scan_wifi_devices()
#                 speak(f"Found {len(devices)} devices on your network")

#                 for ip, mac, name, vendor in devices:
#                     brand, dtype = detect_brand(vendor)
#                     brand_clean  = brand.split()[-1]
#                     speak(f"{brand_clean} device at IP {ip}")

#                 risk = network_map(devices)
#                 intrusion_detection(devices)

#                 for ip, mac, name, vendor in devices:
#                     port_scan(ip)

#                 threat = ai_threat_prediction(devices)
#                 soc_dashboard(devices, threat)
#                 network_graph(devices)

#                 speak(f"Scan complete. {len(devices)} devices found. Network risk level is {risk}")

#             elif "packet sniffer" in command:
#                 speak("Starting packet sniffer")
#                 start_sniffer()

#             elif any(word in command for word in ["exit", "stop", "quit", "bye"]):
#                 speak("Goodbye sir")
#                 break

#         except:
#             continue

# # ══════════════════════════════════════════════════
# # ✅ START — HUD automatically launch hogi
# # ══════════════════════════════════════════════════
# print(f"{C.CYAN}{C.BOLD}[JARVIS] Starting... Iron Man HUD launching!{C.RESET}")
# threading.Thread(target=launch_hud, daemon=True).start()  # ← Auto HUD

# voice_thread        = threading.Thread(target=jarvis_loop)
# voice_thread.daemon = True
# voice_thread.start()

# while True:
#     pass