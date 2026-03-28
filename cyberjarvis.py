
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

# # -------- MAC Vendor Lookup --------
# def get_vendor(mac):
#     try:
#         url=f"https://api.macvendors.com/{mac}"
#         response=requests.get(url,timeout=3)
#         if response.status_code==200:
#             return response.text
#         return "Unknown Vendor"
#     except:
#         return "Unknown Vendor"

# # -------- Device Brand Detection --------
# def detect_brand(vendor):
#     vendor=vendor.lower()
#     if "samsung" in vendor:
#         return "Samsung Phone"
#     elif "apple" in vendor:
#         return "iPhone / Apple Device"
#     elif "xiaomi" in vendor or "redmi" in vendor:
#         return "Xiaomi Phone"
#     elif "oppo" in vendor:
#         return "Oppo Phone"
#     elif "vivo" in vendor:
#         return "Vivo Phone"
#     elif "realme" in vendor:
#         return "Realme Phone"
#     elif "amazon" in vendor:
#         return "Alexa / Fire TV"
#     elif "intel" in vendor:
#         return "Laptop / PC"
#     elif "huawei" in vendor:
#         return "Huawei Device"
#     else:
#         return "Unknown Device"

# # -------- WiFi Scan --------
# def scan_wifi_devices():
#     hostname=socket.gethostname()
#     local_ip=socket.gethostbyname(hostname)
#     parts=local_ip.split(".")
#     subnet=parts[0]+"."+parts[1]+"."+parts[2]+".0/24"
#     print("Scanning subnet:",subnet)

#     arp=ARP(pdst=subnet)
#     ether=Ether(dst="ff:ff:ff:ff:ff:ff")
#     packet=ether/arp

#     result=srp(packet,timeout=3,verbose=0)[0]
#     devices=[]

#     for sent,received in result:
#         ip=received.psrc
#         mac=received.hwsrc
#         try:
#             name=socket.gethostbyaddr(ip)[0]
#         except:
#             name="Unknown"

#         vendor=get_vendor(mac)
#         devices.append((ip,mac,name,vendor))

#     return devices

# # -------- Port Scanner --------
# def port_scan(ip):
#     print("\nPort Scanning:",ip)
#     open_ports=[]
#     for port in range(20,1025):
#         s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#         s.settimeout(0.5)
#         result=s.connect_ex((ip,port))
#         if result==0:
#             print("Open Port:",port)
#             open_ports.append(port)
#         s.close()
#     return open_ports

# # -------- Suspicious Traffic Detection --------
# traffic_counter={}

# # -------- Hacker Location Finder --------
# def get_hacker_location(ip):
#     try:
#         url = f"http://ip-api.com/json/{ip}"
#         response = requests.get(url).json()

#         city = response.get("city","Unknown")
#         country = response.get("country","Unknown")
#         isp = response.get("isp","Unknown")
#         lat = response.get("lat")
#         lon = response.get("lon")

#         print("\n🌍 Hacker Location")
#         print("City:", city)
#         print("Country:", country)
#         print("ISP:", isp)

#         return lat,lon

#     except:
#         print("Location not found")
#         return None,None

# # -------- Attack Map --------
# def show_attack_map(lat,lon):
#     if lat and lon:
#         url=f"https://www.google.com/maps?q={lat},{lon}"
#         print("Opening attack location on Google Map...")
#         webbrowser.open(url)

# # -------- ARP Spoofing Detection --------
# arp_table={}
# # -------- Auto IP Blocker --------
# def block_ip(ip):
#     try:
#         import os
#         print("Blocking attacker IP:", ip)
#         os.system(f'netsh advfirewall firewall add rule name="Block_{ip}" dir=in action=block remoteip={ip}')
#         print("IP Blocked Successfully")
#     except:
#         print("Failed to block IP")

# # -------- DDoS Detection --------
# ddos_counter={}

# # -------- Packet Sniffer --------
# def packet_callback(packet):

#     if packet.haslayer(ARP) and packet[ARP].op==2:

#         ip=packet[ARP].psrc
#         mac=packet[ARP].hwsrc

#         if ip in arp_table:
#             if arp_table[ip] != mac:
#                 print("⚠ Possible ARP Spoofing Attack Detected")
#                 print("IP:",ip)
#                 print("Real MAC:",arp_table[ip])
#                 print("Fake MAC:",mac)
#         else:
#             arp_table[ip]=mac

#     if packet.haslayer("IP"):

#         src=packet["IP"].src
#         dst=packet["IP"].dst

#         print("Packet:",src,"->",dst)

#         if src not in traffic_counter:
#             traffic_counter[src]=0

#         traffic_counter[src]+=1

#         if traffic_counter[src] > 20:
#             print("⚠ Suspicious Traffic Detected from",src)
#             lat,lon=get_hacker_location(src)
#             show_attack_map(lat,lon)

#         if src not in ddos_counter:
#             ddos_counter[src]=0

#         ddos_counter[src]+=1

#         if ddos_counter[src] > 50:
#             print("⚠ Possible DDoS / Flood Attack")
#             print("Attacker IP:",src)
#             print("Packets Sent:",ddos_counter[src])
#             lat,lon=get_hacker_location(src)
#             show_attack_map(lat,lon)
#             block_ip(src)

# def start_sniffer():
#     print("\nStarting Packet Sniffer...")
#     sniff(prn=packet_callback,count=10)

# # -------- Intrusion Detection --------
# known_devices=[]

# def intrusion_detection(devices):
#     print("\nIntrusion Detection")
#     for ip,mac,name,vendor in devices:
#         if mac not in known_devices:
#             print("⚠ Unknown Device Detected")
#             print("IP:",ip)
#             print("MAC:",mac)
#             print("Vendor:",vendor)

# # -------- AI Threat Prediction --------
# def ai_threat_prediction(devices):
#     unknown=0
#     for ip,mac,name,vendor in devices:
#         brand=detect_brand(vendor)
#         if brand=="Unknown Device":
#             unknown+=1

#     score=0
#     if unknown>2:
#         score+=2
#     if len(devices)>8:
#         score+=1

#     if score>=3:
#         threat="High"
#     elif score>=1:
#         threat="Medium"
#     else:
#         threat="Low"

#     print("\nAI Threat Level:",threat)
#     return threat

# # -------- Network Map --------
# def network_map(devices):
#     print("\nNetwork Map")
#     unknown=0

#     for ip,mac,name,vendor in devices:
#         brand=detect_brand(vendor)
#         print("Device:",brand,"| IP:",ip)

#         if brand=="Unknown Device":
#             unknown+=1

#     risk="Low"

#     if unknown>2:
#         risk="High"
#     elif unknown>0:
#         risk="Medium"

#     print("\nNetwork Risk Level:",risk)
#     return risk

# # -------- Network Graph --------
# def network_graph(devices):
#     G=nx.Graph()
#     router="Router"
#     G.add_node(router)

#     for ip,mac,name,vendor in devices:
#         device=f"{name}\n{ip}"
#         G.add_node(device)
#         G.add_edge(router,device)

#     pos=nx.spring_layout(G)
#     nx.draw(G,pos,with_labels=True)
#     plt.title("Network Device Map")
#     plt.show()

# # -------- SOC Dashboard --------
# def soc_dashboard(devices,threat):
#     cpu=psutil.cpu_percent()
#     ram=psutil.virtual_memory().percent

#     print("\nCYBER AI SOC DASHBOARD")
#     print("----------------------")
#     print("CPU Usage:",cpu,"%")
#     print("RAM Usage:",ram,"%")
#     print("Connected Devices:",len(devices))
#     print("Threat Level:",threat)

# # -------- Voice Loop --------
# def jarvis_loop():

#     pythoncom.CoInitialize()
#     speaker=win32com.client.Dispatch("SAPI.SpVoice")
#     cyber=CyberAI()

#     def speak(text):
#         print("Jarvis:",text)
#         speaker.Speak(text)

#     recognizer=sr.Recognizer()
#     mic=sr.Microphone()

#     with mic as source:
#         recognizer.adjust_for_ambient_noise(source,duration=1)

#     speak("Jarvis is online tell me sir")

#     while True:
#         try:
#             with mic as source:
#                 print("Listening...")
#                 audio=recognizer.listen(source,timeout=5,phrase_time_limit=5)

#             command=recognizer.recognize_google(audio,language="en-IN").lower().strip()
#             print("You said:",command)

#             if "system status" in command:
#                 speak("Checking system status")
#                 cyber.cpu_usage()
#                 cyber.ram_usage()

#             elif "scan network" in command:

#                 speak("Scanning network devices")
#                 devices=scan_wifi_devices()

#                 risk=network_map(devices)
#                 intrusion_detection(devices)

#                 for ip,mac,name,vendor in devices:
#                     port_scan(ip)

#                 threat=ai_threat_prediction(devices)
#                 soc_dashboard(devices,threat)
#                 network_graph(devices)

#                 speak(f"Network risk level is {risk}")

#             elif "packet sniffer" in command:
#                 speak("Starting packet sniffer")
#                 start_sniffer()

#             elif any(word in command for word in ["exit","stop","quit","bye"]):
#                 speak("Goodbye sir")
#                 break

#         except:
#             continue

# voice_thread=threading.Thread(target=jarvis_loop)
# voice_thread.daemon=True
# voice_thread.start()

# while True:
#     pass



#*******************#



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
# import concurrent.futures
# from ddos_trecker import check_ddos, show_all_attackers
# from Dashboard import start_dashboard
# from password_checker import check_password
# from wifi_deauth_detector import start_deauth_monitor, stop_deauth_monitor
# from mac_spoof_detector import check_mac_spoofing
# import subprocess
# from email_breach import check_email_breach

# # 🔥 NEW IMPORTS
# import folium
# import speedtest

# from evil_twin_detector  import (start_evil_twin_monitor,
#                                   stop_evil_twin_monitor,
#                                   show_evil_twin_report)
# from ml_anomaly_detector import (start_anomaly_detector,
#                                   stop_anomaly_detector,
#                                   get_anomaly_report)
# from face_auth import start_face_auth
# import security_utils
# import fake_update
# import cv2
# from voice_auth import verify_voice
# import pythoncom
# import time

# # -------- GLOBALS --------
# previous_devices = set()


# # -------- Smart Device Name — 4 methods --------
# def get_device_name(ip, mac, vendor):
#     """
#     4 methods se real device name dhundho — RAM only
#     """

#     # Method 1 — Reverse DNS hostname
#     try:
#         hostname = socket.gethostbyaddr(ip)[0]
#         if hostname and hostname != ip:
#             return hostname
#     except:
#         pass

#     # Method 2 — NetBIOS (Windows devices)
#     try:
#         result = subprocess.run(
#             ["nbtstat", "-A", ip],
#             capture_output=True, text=True, timeout=3
#         )
#         for line in result.stdout.splitlines():
#             if "<00>" in line and "UNIQUE" in line:
#                 nb_name = line.strip().split()[0]
#                 if nb_name:
#                     return nb_name
#     except:
#         pass

#     # Method 3 — Vendor se smart name
#     v = vendor.lower().strip()
#     last = ip.split(".")[-1]

#     brand_map = {
#         "samsung"   : f"Samsung-{last}",
#         "apple"     : f"Apple-{last}",
#         "iphone"    : f"iPhone-{last}",
#         "ipad"      : f"iPad-{last}",
#         "macbook"   : f"MacBook-{last}",
#         "xiaomi"    : f"Xiaomi-{last}",
#         "redmi"     : f"Redmi-{last}",
#         "oppo"      : f"Oppo-{last}",
#         "vivo"      : f"Vivo-{last}",
#         "realme"    : f"Realme-{last}",
#         "oneplus"   : f"OnePlus-{last}",
#         "intel"     : f"Laptop-{last}",
#         "dell"      : f"Dell-PC-{last}",
#         "hp"        : f"HP-PC-{last}",
#         "hewlett"   : f"HP-PC-{last}",
#         "lenovo"    : f"Lenovo-{last}",
#         "asus"      : f"Asus-{last}",
#         "acer"      : f"Acer-{last}",
#         "huawei"    : f"Huawei-{last}",
#         "amazon"    : f"Alexa-{last}",
#         "google"    : f"Google-{last}",
#         "tp-link"   : f"TPLink-Router-{last}",
#         "tplink"    : f"TPLink-Router-{last}",
#         "d-link"    : f"DLink-Router-{last}",
#         "dlink"     : f"DLink-Router-{last}",
#         "netgear"   : f"Netgear-Router-{last}",
#         "zyxel"     : f"ZyXEL-Router-{last}",
#         "cisco"     : f"Cisco-{last}",
#         "jio"       : f"JioFi-{last}",
#         "reliance"  : f"Jio-{last}",
#         "bsnl"      : f"BSNL-{last}",
#         "nokia"     : f"Nokia-{last}",
#         "motorola"  : f"Moto-{last}",
#         "sony"      : f"Sony-{last}",
#         "lg"        : f"LG-{last}",
#         "microsoft" : f"MS-Surface-{last}",
#         "raspberry" : f"RaspberryPi-{last}",
#     }

#     for key, name in brand_map.items():
#         if key in v:
#             return name

#     # Method 4 — Vendor hai but specific nahi
#     if v and "unknown" not in v:
#         short = vendor.strip()[:10]
#         return f"{short}-{last}"

#     # Kuch nahi mila
#     return f"Device-{last}"


# # -------- MAC Vendor Lookup --------
# def get_vendor(mac):
#     try:
#         url = f"https://api.macvendors.com/{mac}"
#         response = requests.get(url, timeout=3)
#         if response.status_code == 200:
#             return response.text
#         return "Unknown Vendor"
#     except:
#         return "Unknown Vendor"


# # -------- Device Brand Detection --------
# def detect_brand(vendor):
#     vendor = vendor.lower()
#     if "samsung" in vendor:
#         return "Samsung Phone"
#     elif "apple" in vendor:
#         return "iPhone / Apple Device"
#     elif "xiaomi" in vendor or "redmi" in vendor:
#         return "Xiaomi Phone"
#     elif "oppo" in vendor:
#         return "Oppo Phone"
#     elif "vivo" in vendor:
#         return "Vivo Phone"
#     elif "realme" in vendor:
#         return "Realme Phone"
#     elif "amazon" in vendor:
#         return "Alexa / Fire TV"
#     elif "intel" in vendor:
#         return "Laptop / PC"
#     elif "huawei" in vendor:
#         return "Huawei Device"
#     else:
#         return "Unknown Device"


# # -------- UPGRADED WiFi Scan --------
# def scan_wifi_devices():
#     hostname = socket.gethostname()
#     local_ip = socket.gethostbyname(hostname)
#     parts    = local_ip.split(".")
#     subnet   = parts[0] + "." + parts[1] + "." + parts[2] + ".0/24"
#     print(f"\nScanning subnet: {subnet}")
#     print("─" * 50)

#     arp    = ARP(pdst=subnet)
#     ether  = Ether(dst="ff:ff:ff:ff:ff:ff")
#     packet = ether / arp

#     result  = srp(packet, timeout=3, verbose=0)[0]
#     devices = []

#     for sent, received in result:
#         ip  = received.psrc
#         mac = received.hwsrc

#         print(f"  Found   : {ip} ({mac})")
#         print(f"  Recognizing...")

#         vendor = get_vendor(mac)
#         name   = get_device_name(ip, mac, vendor)
#         brand  = detect_brand(vendor)

#         print(f"  Device  : {name}")
#         print(f"  Brand   : {brand}")
#         print(f"  Vendor  : {vendor.strip()}")
#         print("  " + "─" * 46)

#         devices.append((ip, mac, name, vendor))

#     print(f"\n  Total devices found: {len(devices)}")
#     print("─" * 50)

#     return devices


# # -------- NEW: LIVE ATTACK MAP --------
# def show_live_attack_map():
#     from ddos_trecker import tracked_ips

#     if not tracked_ips:
#         print("No attackers to show")
#         return

#     m = folium.Map(location=[20.5937, 78.9629], zoom_start=4)

#     for ip, loc in tracked_ips.items():
#         if loc.get("lat") and loc.get("lon"):
#             folium.Marker(
#                 location=[loc["lat"], loc["lon"]],
#                 popup=f"{ip} - {loc['city']}, {loc['country']}",
#                 icon=folium.Icon(color="red")
#             ).add_to(m)

#     m.save("attack_map.html")
#     webbrowser.open("attack_map.html")


# # -------- NEW: INTERNET SPEED --------
# def check_internet_speed():
#     try:
#         print("Checking internet speed... please wait")

#         st = speedtest.Speedtest()

#         st.get_best_server()   # 🔥 IMPORTANT FIX

#         download = st.download() / 1_000_000
#         upload   = st.upload() / 1_000_000

#         print(f"Download: {download:.2f} Mbps")
#         print(f"Upload: {upload:.2f} Mbps")

#         return download, upload

#     except Exception as e:
#         print("Speed test failed:", e)
#         return 0, 0

# # -------- Port Scanner — FAST --------
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
#     print("\nPort Scanning:", ip)
#     open_ports = []
#     args = [(ip, p) for p in range(20, 1025)]

#     with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
#         results = executor.map(_check_one_port, args)

#     for port in results:
#         if port:
#             print("Open Port:", port)
#             open_ports.append(port)

#     return open_ports


# # -------- Suspicious Traffic Detection --------
# traffic_counter = {}


# # -------- Hacker Location Finder --------
# def get_hacker_location(ip):
#     try:
#         url      = f"http://ip-api.com/json/{ip}"
#         response = requests.get(url).json()

#         city    = response.get("city", "Unknown")
#         country = response.get("country", "Unknown")
#         isp     = response.get("isp", "Unknown")
#         lat     = response.get("lat")
#         lon     = response.get("lon")

#         print("\n🌍 Hacker Location")
#         print("City:", city)
#         print("Country:", country)
#         print("ISP:", isp)

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
#         import os
#         print("Blocking attacker IP:", ip)
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
#                 print("⚠ Possible ARP Spoofing Attack Detected")
#                 print("IP:", ip)
#                 print("Real MAC:", arp_table[ip])
#                 print("Fake MAC:", mac)
#         else:
#             arp_table[ip] = mac

#     if packet.haslayer("IP"):

#         src = packet["IP"].src
#         dst = packet["IP"].dst

#         print("Packet:", src, "->", dst)

#         if src not in traffic_counter:
#             traffic_counter[src] = 0

#         traffic_counter[src] += 1

#         if traffic_counter[src] > 20:
#             print("⚠ Suspicious Traffic Detected from", src)
#             lat, lon = get_hacker_location(src)
#             show_attack_map(lat, lon)

#         check_ddos(src, speaker)


# def start_sniffer():
#     print("\nStarting Packet Sniffer...")
#     sniff(prn=packet_callback, count=10)


# # -------- Intrusion Detection --------
# known_devices = []

# def intrusion_detection(devices):
#     print("\nIntrusion Detection")
#     for ip, mac, name, vendor in devices:
#         if mac not in known_devices:
#             print("⚠ Unknown Device Detected")
#             print("IP:", ip)
#             print("MAC:", mac)
#             print("Vendor:", vendor)


# # -------- AI Threat Prediction --------
# def ai_threat_prediction(devices):
#     unknown = 0
#     for ip, mac, name, vendor in devices:
#         brand = detect_brand(vendor)
#         if brand == "Unknown Device":
#             unknown += 1

#     score = 0
#     if unknown > 2:
#         score += 2
#     if len(devices) > 8:
#         score += 1

#     if score >= 3:
#         threat = "High"
#     elif score >= 1:
#         threat = "Medium"
#     else:
#         threat = "Low"

#     print("\nAI Threat Level:", threat)
#     return threat


# # -------- Network Map --------
# def network_map(devices):
#     print("\nNetwork Map")
#     unknown = 0

#     for ip, mac, name, vendor in devices:
#         brand = detect_brand(vendor)
#         print("Device:", name, "| Brand:", brand, "| IP:", ip)

#         if brand == "Unknown Device":
#             unknown += 1

#     risk = "Low"

#     if unknown > 2:
#         risk = "High"
#     elif unknown > 0:
#         risk = "Medium"

#     print("\nNetwork Risk Level:", risk)
#     return risk


# # -------- Network Graph --------
# def network_graph(devices):
#     G      = nx.Graph()
#     router = "Router"
#     G.add_node(router)

#     for ip, mac, name, vendor in devices:
#         device = f"{name}\n{ip}"
#         G.add_node(device)
#         G.add_edge(router, device)

#     pos = nx.spring_layout(G)
#     nx.draw(G, pos, with_labels=True)
#     plt.title("Network Device Map")
#     plt.show()


# # -------- SOC Dashboard --------
# def soc_dashboard(devices, threat):
#     cpu = psutil.cpu_percent()
#     ram = psutil.virtual_memory().percent

#     print("\nCYBER AI SOC DASHBOARD")
#     print("----------------------")
#     print("CPU Usage:", cpu, "%")
#     print("RAM Usage:", ram, "%")
#     print("Connected Devices:", len(devices))
#     print("Threat Level:", threat)


# # -------- speaker global --------
# speaker = None


# # -------- Voice Loop --------
# def jarvis_loop():

#     global speaker, previous_devices
#     pythoncom.CoInitialize()
#     speaker = win32com.client.Dispatch("SAPI.SpVoice")
#     cyber   = CyberAI()

#     # RAM mein last scan store hoga — MAC spoof check ke liye
#     last_devices = []

#     def speak(text):
#         print("Jarvis:", text)
#         if dash: dash.set_mode("speaking")
#         speaker.Speak(text)
#         if dash: dash.set_mode("listening")

#     recognizer = sr.Recognizer()
#     mic        = sr.Microphone()

#     with mic as source:
#         recognizer.adjust_for_ambient_noise(source, duration=1)

#     speak("Jarvis is online tell me sir")

#     while True:
#         try:
#             if dash: dash.set_mode("listening")

#             with mic as source:
#                 print("Listening...")
#                 if dash: dash.set_mode("listening")
#                 audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
#             print("Recognizing...")
#             if dash: dash.set_mode("processing")

#             command = recognizer.recognize_google(audio, language="en-IN").lower().strip()
#             print("You said:", command)

#             if dash: dash.set_command(command)

#             if "jarvis" in command and len(command.split()) == 1:
#                 active = True
#                 speak("Yes sir")

#             elif "scan network" in command:
#                 speak("Scanning network sir")
#                 devices = scan_wifi_devices()

#                 # RAM mein save karo — MAC spoof ke liye baad mein use hoga
#                 last_devices = devices

#                 # 🔥 NEW DEVICE DETECTION
#                 current_devices = set([mac for ip, mac, name, vendor in devices])
#                 new_devices = current_devices - previous_devices

#                 for ip, mac, name, vendor in devices:
#                     if mac in new_devices:
#                         speak(f"New device detected {name}")

#                 previous_devices = current_devices

#                 network_map(devices)

#             elif "attack map" in command:
#                 speak("Opening live attack map sir")
#                 show_live_attack_map()
#             elif "start evil twin" in command:
#                speak("Starting Evil Twin attack monitor sir")
#                start_evil_twin_monitor(speaker=speaker, dash=dash)
#             elif "stop evil twin" in command:
#                speak("Stopping Evil Twin monitor sir")
#                stop_evil_twin_monitor(speaker=speaker, dash=dash)
#             elif "evil twin report" in command:
#                speak("Showing Evil Twin report sir")
#                show_evil_twin_report()

#            # ---- ML ANOMALY ----#
#             elif "start anomaly" in command or "start ml" in command:
#                 speak("Starting ML anomaly detection. Learning phase takes 5 minutes sir.")
#                 start_anomaly_detector(speaker=speaker, dash=dash)
#             elif "stop anomaly" in command:
#                 speak("Stopping anomaly detection sir")
#                 stop_anomaly_detector(speaker=speaker, dash=dash)
#             elif "anomaly report" in command:
#                 speak("Showing anomaly report sir")
#                 r = get_anomaly_report()
#                 speak(f"Total {r['total_anomalies']} anomalies detected from {r['total_ips']} IPs sir")

#             elif "internet speed" in command:
#                 speak("Checking internet speed sir")
#                 d, u = check_internet_speed()
#                 speak(f"Download speed is {int(d)} Mbps and upload is {int(u)} Mbps")

#                  # -------- MY IP --------
#             elif "my ip" in command:
#                 speak("Checking your IP address sir")
#                 try:
#                     local_ip = socket.gethostbyname(socket.gethostname())
#                     data    = requests.get("http://ip-api.com/json/", timeout=5).json()
#                     pub_ip  = data.get("query",   "Unknown")
#                     city    = data.get("city",    "Unknown")
#                     country = data.get("country", "Unknown")
#                     isp     = data.get("isp",     "Unknown")
#                     print("[ MY IP INFO ]")
#                     print("─" * 35)
#                     print(f"  Local IP  : {local_ip}")
#                     print(f"  Public IP : {pub_ip}")
#                     print(f"  City      : {city}")
#                     print(f"  Country   : {country}")
#                     print(f"  ISP       : {isp}")
#                     print("─" * 35)
#                     if dash: dash.set_command(f"IP: {pub_ip}")
#                     speak(f"Sir your local IP is {local_ip}. Public IP is {pub_ip}. Location is {city}, {country}. ISP is {isp}.")
#                 except:
#                     speak("Sorry sir, could not fetch IP information")
 

#             elif "check password" in command:
#                     check_password(None, speaker, dash)

#             # -------- DEAUTH MONITOR --------
#             elif "start deauth monitor" in command:
#                 speak("Starting WiFi deauth attack monitor sir")
#                 start_deauth_monitor(speaker, dash)

#             elif "stop deauth monitor" in command:
#                 speak("Stopping WiFi deauth monitor sir")
#                 stop_deauth_monitor(speaker, dash)

#             # -------- MAC SPOOF CHECK --------
#             elif "check mac spoofing" in command:
#                 if last_devices:
#                     speak("Checking MAC spoofing on all devices sir")
#                     check_mac_spoofing(last_devices, speaker, dash)
#                 else:
#                     speak("Sir please scan network first then check MAC spoofing")
#             elif "check email" in command:
#                 check_email_breach(speaker, dash)

#             elif any(word in command for word in ["exit", "stop", "quit", "bye"]):
#                 speak("Goodbye sir")
#                 break


#             else:
#                 speak("Sorry sir command not recognized")

#         except:
#             continue

# dash = start_dashboard()

# print("🔐 Starting Secure Authentication...")

# pythoncom.CoInitialize()
# speak_temp = win32com.client.Dispatch("SAPI.SpVoice")

# # --- STEP 1: Face Authentication ---
# # Note: start_face_auth() ko fast rakhein (sirf 1-2 frames check karein)
# face_ok = start_face_auth()

# if face_ok:
#     # CASE 1: Face match ho gaya
#     print("✅ Welcome back, Sir. Access Granted.")
#     speak_temp.Speak("Welcome back Sir. Access granted.")
    
#     # Jarvis Loop Start
#     threading.Thread(target=jarvis_loop, daemon=True).start()
#     while True:
#         time.sleep(1)

# else:
#     # CASE 2: Face fail — Voice se try karo
#     print("❌ Face not recognized. Trying voice verification...")
#     speak_temp.Speak("Face not recognized. Please verify your voice sir.")

#     from voice_auth import verify_voice
#     # Voice verification engine call
#     voice_ok, msg = verify_voice(speaker=speak_temp)

#     if voice_ok:
#         # CASE 2A: Voice match ho gaya
#         print("✅ Voice Verified. Welcome back Sir. Access Granted.")
#         speak_temp.Speak("Voice verified. Welcome back Sir. Access granted.")
        
#         threading.Thread(target=jarvis_loop, daemon=True).start()
#         while True:
#             time.sleep(1)

#     else:
#         # CASE 3: DONO FAIL — INTRUDER DETECTED!
#         print("\n🚨 [ALERT] Unauthorized Access Detected!")
#         print("Initializing System Core... Please wait.")
#         speak_temp.Speak("Access denied. Intruder detected. Locking system.")

#         # 1. SILENT PHOTO CAPTURE (Ab yahan capture karega jab dono fail ho gaye)
#         # Fast capture using CAP_DSHOW
#         cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#         ret, intruder_frame = cap.read()
#         if ret:
#             security_utils.capture_intruder(intruder_frame) # Logs mein save hoga
#         cap.release()

#         # 2. Acoustic Check (Optional logging of background noise)
#         voice_status = security_utils.check_voice_presence(duration=3)

#         # 3. FAKE LOCKDOWN (Full Screen Update)
#         # Make sure fake_update.py uses root.attributes('-fullscreen', True)
#         fake_update.start_fake_update()

#         print("System Lockdown Active. Goodbye.")



#***********************
import speech_recognition as sr
import threading
import pythoncom
import win32com.client
import socket
import requests
from scapy.all import ARP, Ether, srp, sniff
from cyberai import CyberAI
import psutil
import networkx as nx
import matplotlib.pyplot as plt
from twilio.rest import Client
import webbrowser
import concurrent.futures
from ddos_trecker import check_ddos, show_all_attackers
from Dashboard import start_dashboard
from password_checker import check_password
from wifi_deauth_detector import start_deauth_monitor, stop_deauth_monitor
from mac_spoof_detector import check_mac_spoofing
import subprocess
from email_breach import check_email_breach
import folium
import speedtest
from evil_twin_detector  import (start_evil_twin_monitor,
                                  stop_evil_twin_monitor,
                                  show_evil_twin_report)
from ml_anomaly_detector import (start_anomaly_detector,
                                  stop_anomaly_detector,
                                  get_anomaly_report)
from face_auth import start_face_auth
import security_utils
import fake_update
import cv2
from voice_auth import verify_voice
import time

# ── Fast startup: MAC vendor DB load background mein ──
try:
    from mac_vendor_lookup import MacLookup
    _mac_db = MacLookup()
    threading.Thread(target=_mac_db.update_vendors, daemon=True).start()
    _LOCAL_DB = True
except:
    _mac_db   = None
    _LOCAL_DB = False

# ── Offline OUI fallback (top Indian + global brands) ──
_OUI_MAP = {
    "B4:E6:2D":"Apple",    "F8:FF:C2":"Apple",    "3C:15:C2":"Apple",
    "A4:C3:F0":"Apple",    "E4:AB:89":"Samsung",  "8C:BE:BE":"Samsung",
    "4C:BC:98":"Samsung",  "F4:60:E2":"Xiaomi",   "28:6C:07":"Xiaomi",
    "00:9E:C8":"Xiaomi",   "7C:B0:C2":"Realme",   "64:A2:F9":"Oppo",
    "B0:D5:CC":"Vivo",     "F8:72:EA":"OnePlus",  "80:EA:96":"Jio",
    "14:CF:92":"TP-Link",  "50:C7:BF":"TP-Link",  "C8:3A:35":"Tenda",
    "74:DA:DA":"D-Link",   "1C:AF:F7":"D-Link",   "20:E5:2A":"Netgear",
    "DC:A6:32":"Raspberry Pi","B8:27:EB":"Raspberry Pi",
    "AC:CF:85":"Intel",    "8C:8D:28":"Intel",    "18:56:80":"Intel",
    "FC:64:BA":"Huawei",   "54:89:98":"Huawei",   "00:E0:FC":"Huawei",
    "CC:46:D6":"Cisco",    "00:1A:2B":"Cisco",    "00:50:56":"VMware",
}

# -------- GLOBALS --------
previous_devices = set()


# -------- UPGRADED: MAC Vendor Lookup (3 methods, fast) --------
def get_vendor(mac):
    # Method 1: Offline OUI map (instant)
    prefix = mac.upper()[:8]
    if prefix in _OUI_MAP:
        return _OUI_MAP[prefix]

    # Method 2: Local database (offline)
    if _mac_db:
        try:
            v = _mac_db.lookup(mac)
            if v and len(v) > 2:
                return v
        except:
            pass

    # Method 3: API (last resort, fast timeout)
    try:
        r = requests.get(f"https://api.macvendors.com/{mac}", timeout=1.5)
        if r.status_code == 200 and r.text.strip():
            return r.text.strip()
    except:
        pass

    return "Unknown Vendor"


# -------- UPGRADED: Smart Device Name (5 methods) --------
def get_device_name(ip, mac, vendor):
    import re
    last = ip.split(".")[-1]
    v    = (vendor or "").lower().strip()

    # Method 1: Reverse DNS
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        if hostname and hostname != ip and not hostname.startswith(ip):
            name = hostname.split(".")[0]
            if len(name) > 2:
                return name
    except:
        pass

    # Method 2: NetBIOS (Windows)
    try:
        result = subprocess.run(
            ["nbtstat", "-A", ip],
            capture_output=True, text=True, timeout=2
        )
        for line in result.stdout.splitlines():
            if "<00>" in line and "UNIQUE" in line:
                parts = line.strip().split()
                if parts and len(parts[0]) > 1:
                    return parts[0]
    except:
        pass

    # Method 3: ARP table
    try:
        result = subprocess.run(
            ["arp", "-a", ip],
            capture_output=True, text=True, timeout=2
        )
        for line in result.stdout.splitlines():
            if ip in line:
                parts = line.split()
                if parts and re.match(r'^[a-zA-Z][a-zA-Z0-9\-]{2,}$', parts[0]):
                    return parts[0]
    except:
        pass

    # Method 4: Vendor brand map
    brand_map = {
        "samsung":"Samsung","apple":"Apple","iphone":"iPhone",
        "ipad":"iPad","macbook":"MacBook","xiaomi":"Xiaomi",
        "redmi":"Redmi","oppo":"Oppo","vivo":"Vivo",
        "realme":"Realme","oneplus":"OnePlus","intel":"Laptop",
        "dell":"Dell-PC","hp":"HP-PC","hewlett":"HP-PC",
        "lenovo":"Lenovo","asus":"Asus","acer":"Acer",
        "huawei":"Huawei","amazon":"Alexa","google":"Google",
        "tp-link":"TPLink-Router","tplink":"TPLink-Router",
        "tenda":"Tenda-Router","d-link":"DLink-Router",
        "dlink":"DLink-Router","netgear":"Netgear",
        "zyxel":"ZyXEL","cisco":"Cisco","jio":"JioFi",
        "reliance":"Jio","bsnl":"BSNL","nokia":"Nokia",
        "motorola":"Moto","sony":"Sony","lg":"LG",
        "microsoft":"Surface","raspberry":"RaspPi",
        "espressif":"IoT-Device","realtek":"Laptop",
    }
    for key, name in brand_map.items():
        if key in v:
            return f"{name}-{last}"

    # Method 5: Short vendor
    if v and "unknown" not in v and len(v) > 2:
        clean = re.sub(r'[^a-zA-Z0-9]', '', vendor.strip())[:10]
        return f"{clean}-{last}"

    return f"Device-{last}"


# -------- UPGRADED: Device Brand Detection --------
def detect_brand(vendor):
    if not vendor:
        return "Unknown Device"
    v = vendor.lower()
    brands = [
        ("samsung","Samsung Phone"),("apple","Apple Device"),
        ("iphone","iPhone"),("ipad","iPad"),
        ("xiaomi","Xiaomi Phone"),("redmi","Redmi Phone"),
        ("oppo","Oppo Phone"),("vivo","Vivo Phone"),
        ("realme","Realme Phone"),("oneplus","OnePlus Phone"),
        ("amazon","Alexa / Fire TV"),("intel","Laptop / PC"),
        ("realtek","Laptop / PC"),("huawei","Huawei Device"),
        ("tp-link","TP-Link Router"),("tplink","TP-Link Router"),
        ("tenda","Tenda Router"),("d-link","D-Link Router"),
        ("dlink","D-Link Router"),("netgear","Netgear Router"),
        ("zyxel","ZyXEL Router"),("cisco","Cisco Device"),
        ("jio","JioFi Device"),("espressif","IoT Device"),
        ("raspberry","Raspberry Pi"),("dell","Dell Laptop"),
        ("hp","HP Laptop"),("hewlett","HP Laptop"),
        ("lenovo","Lenovo Device"),("asus","Asus Device"),
        ("acer","Acer Device"),("google","Google Device"),
        ("motorola","Motorola Phone"),("nokia","Nokia Device"),
        ("sony","Sony Device"),("lg","LG Device"),
        ("microsoft","Microsoft Surface"),
    ]
    for key, brand in brands:
        if key in v:
            return brand
    return "Unknown Device"


# -------- UPGRADED: WiFi Scan (parallel, fast, colored) --------
def scan_wifi_devices():
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)
        USE_COLOR = True
    except:
        USE_COLOR = False

    def c(color, text):
        if USE_COLOR:
            colors = {"cyan":"\033[96m","green":"\033[92m",
                      "yellow":"\033[93m","red":"\033[91m",
                      "white":"\033[97m","dim":"\033[2m","reset":"\033[0m"}
            return colors.get(color,"") + text + colors["reset"]
        return text

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    parts    = local_ip.split(".")
    subnet   = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"

    print(f"\n  {c('cyan','Scanning:')} {subnet}")
    print("  " + "─" * 52)

    arp    = ARP(pdst=subnet)
    ether  = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]
    raw    = [(r.psrc, r.hwsrc) for _, r in result]

    if not raw:
        print(f"  {c('yellow','No devices found.')}")
        return []

    print(f"  Found {c('cyan', str(len(raw)))} device(s) — identifying in parallel...\n")

    def _scan_one(ip, mac):
        vendor = get_vendor(mac)
        name   = get_device_name(ip, mac, vendor)
        brand  = detect_brand(vendor)
        return ip, mac, name, vendor, brand

    devices = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        futs = {ex.submit(_scan_one, ip, mac): (ip, mac) for ip, mac in raw}
        for fut in concurrent.futures.as_completed(futs):
            try:
                ip, mac, name, vendor, brand = fut.result()
                devices.append((ip, mac, name, vendor))
                is_unknown = brand == "Unknown Device"
                marker     = c("yellow","?") if is_unknown else c("green","+")
                name_col   = c("yellow", name) if is_unknown else c("green", name)
                print(f"  [{marker}] {name_col:<28} {c('white',ip):<16} {c('cyan',brand)}")
                print(f"      {c('dim', f'MAC: {mac}  |  Vendor: {vendor[:35]}')}")
                print()
            except Exception as e:
                print(f"  [!] Error: {e}")

    print("  " + "─" * 52)

    unknown = sum(1 for _, _, _, v in devices if detect_brand(v) == "Unknown Device")
    risk    = c("red","HIGH") if unknown > 2 else c("yellow","MEDIUM") if unknown > 0 else c("green","LOW")

    print(f"  Total devices : {c('cyan', str(len(devices)))}")
    print(f"  Network risk  : {risk}\n")

    return devices


# -------- NEW: LIVE ATTACK MAP --------
def show_live_attack_map():
    from ddos_trecker import tracked_ips
    if not tracked_ips:
        print("No attackers to show")
        return
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=4)
    for ip, loc in tracked_ips.items():
        if loc.get("lat") and loc.get("lon"):
            folium.Marker(
                location=[loc["lat"], loc["lon"]],
                popup=f"{ip} - {loc['city']}, {loc['country']}",
                icon=folium.Icon(color="red")
            ).add_to(m)
    m.save("attack_map.html")
    webbrowser.open("attack_map.html")


# -------- NEW: INTERNET SPEED --------
def check_internet_speed():
    try:
        print("Checking internet speed... please wait")
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000
        upload   = st.upload()   / 1_000_000
        print(f"Download: {download:.2f} Mbps")
        print(f"Upload: {upload:.2f} Mbps")
        return download, upload
    except Exception as e:
        print("Speed test failed:", e)
        return 0, 0


# -------- Port Scanner — FAST --------
def _check_one_port(args):
    ip, port = args
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((ip, port))
        s.close()
        return port if result == 0 else None
    except:
        return None

def port_scan(ip):
    print("\nPort Scanning:", ip)
    open_ports = []
    args = [(ip, p) for p in range(20, 1025)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(_check_one_port, args)
    for port in results:
        if port:
            print("Open Port:", port)
            open_ports.append(port)
    return open_ports


# -------- Suspicious Traffic Detection --------
traffic_counter = {}


# -------- Hacker Location Finder --------
def get_hacker_location(ip):
    try:
        url      = f"http://ip-api.com/json/{ip}"
        response = requests.get(url).json()
        city    = response.get("city", "Unknown")
        country = response.get("country", "Unknown")
        isp     = response.get("isp", "Unknown")
        lat     = response.get("lat")
        lon     = response.get("lon")
        print("\n🌍 Hacker Location")
        print("City:", city)
        print("Country:", country)
        print("ISP:", isp)
        return lat, lon
    except:
        print("Location not found")
        return None, None


# -------- Attack Map --------
def show_attack_map(lat, lon):
    if lat and lon:
        url = f"https://www.google.com/maps?q={lat},{lon}"
        print("Opening attack location on Google Map...")
        webbrowser.open(url)


# -------- ARP Spoofing Detection --------
arp_table = {}


# -------- Auto IP Blocker --------
def block_ip(ip):
    try:
        import os
        print("Blocking attacker IP:", ip)
        os.system(f'netsh advfirewall firewall add rule name="Block_{ip}" dir=in action=block remoteip={ip}')
        print("IP Blocked Successfully")
    except:
        print("Failed to block IP")


# -------- DDoS Detection --------
ddos_counter = {}


# -------- Packet Sniffer --------
def packet_callback(packet):
    if packet.haslayer(ARP) and packet[ARP].op == 2:
        ip  = packet[ARP].psrc
        mac = packet[ARP].hwsrc
        if ip in arp_table:
            if arp_table[ip] != mac:
                print("⚠ Possible ARP Spoofing Attack Detected")
                print("IP:", ip)
                print("Real MAC:", arp_table[ip])
                print("Fake MAC:", mac)
        else:
            arp_table[ip] = mac

    if packet.haslayer("IP"):
        src = packet["IP"].src
        dst = packet["IP"].dst
        print("Packet:", src, "->", dst)
        if src not in traffic_counter:
            traffic_counter[src] = 0
        traffic_counter[src] += 1
        if traffic_counter[src] > 20:
            print("⚠ Suspicious Traffic Detected from", src)
            lat, lon = get_hacker_location(src)
            show_attack_map(lat, lon)
        check_ddos(src, speaker)


def start_sniffer():
    print("\nStarting Packet Sniffer...")
    sniff(prn=packet_callback, count=10)


# -------- Intrusion Detection --------
known_devices = []

def intrusion_detection(devices):
    print("\nIntrusion Detection")
    for ip, mac, name, vendor in devices:
        if mac not in known_devices:
            print("⚠ Unknown Device Detected")
            print("IP:", ip)
            print("MAC:", mac)
            print("Vendor:", vendor)


# -------- AI Threat Prediction --------
def ai_threat_prediction(devices):
    unknown = 0
    for ip, mac, name, vendor in devices:
        brand = detect_brand(vendor)
        if brand == "Unknown Device":
            unknown += 1
    score = 0
    if unknown > 2:
        score += 2
    if len(devices) > 8:
        score += 1
    if score >= 3:
        threat = "High"
    elif score >= 1:
        threat = "Medium"
    else:
        threat = "Low"
    print("\nAI Threat Level:", threat)
    return threat


# -------- Network Map --------
def network_map(devices):
    print("\nNetwork Map")
    unknown = 0
    for ip, mac, name, vendor in devices:
        brand = detect_brand(vendor)
        print("Device:", name, "| Brand:", brand, "| IP:", ip)
        if brand == "Unknown Device":
            unknown += 1
    risk = "Low"
    if unknown > 2:
        risk = "High"
    elif unknown > 0:
        risk = "Medium"
    print("\nNetwork Risk Level:", risk)
    return risk


# -------- Network Graph --------
def network_graph(devices):
    G      = nx.Graph()
    router = "Router"
    G.add_node(router)
    for ip, mac, name, vendor in devices:
        device = f"{name}\n{ip}"
        G.add_node(device)
        G.add_edge(router, device)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.title("Network Device Map")
    plt.show()


# -------- SOC Dashboard --------
def soc_dashboard(devices, threat):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    print("\nCYBER AI SOC DASHBOARD")
    print("----------------------")
    print("CPU Usage:", cpu, "%")
    print("RAM Usage:", ram, "%")
    print("Connected Devices:", len(devices))
    print("Threat Level:", threat)


# -------- speaker global --------
speaker = None


# -------- Voice Loop --------
def jarvis_loop():
    global speaker, previous_devices
    pythoncom.CoInitialize()
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    cyber   = CyberAI()
    last_devices = []

    def speak(text):
        print("Jarvis:", text)
        if dash: dash.set_mode("speaking")
        speaker.Speak(text)
        if dash: dash.set_mode("listening")

    recognizer = sr.Recognizer()
    mic        = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    speak("Jarvis is online tell me sir")

    while True:
        try:
            if dash: dash.set_mode("listening")
            with mic as source:
                print("Listening...")
                if dash: dash.set_mode("listening")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            if dash: dash.set_mode("processing")

            command = recognizer.recognize_google(audio, language="en-IN").lower().strip()
            print("You said:", command)
            if dash: dash.set_command(command)

            if "jarvis" in command and len(command.split()) == 1:
                active = True
                speak("Yes sir")

            elif "scan network" in command:
                speak("Scanning network sir")
                devices     = scan_wifi_devices()
                last_devices = devices
                current_devices = set([mac for ip, mac, name, vendor in devices])
                new_devices     = current_devices - previous_devices
                for ip, mac, name, vendor in devices:
                    if mac in new_devices:
                        speak(f"New device detected {name}")
                previous_devices = current_devices
                network_map(devices)

            elif "attack map" in command:
                speak("Opening live attack map sir")
                show_live_attack_map()

            elif "start evil twin" in command:
                speak("Starting Evil Twin attack monitor sir")
                start_evil_twin_monitor(speaker=speaker, dash=dash)

            elif "stop evil twin" in command:
                speak("Stopping Evil Twin monitor sir")
                stop_evil_twin_monitor(speaker=speaker, dash=dash)

            elif "evil twin report" in command:
                speak("Showing Evil Twin report sir")
                show_evil_twin_report()

            elif "start anomaly" in command or "start ml" in command:
                speak("Starting ML anomaly detection. Learning phase takes 5 minutes sir.")
                start_anomaly_detector(speaker=speaker, dash=dash)

            elif "stop anomaly" in command:
                speak("Stopping anomaly detection sir")
                stop_anomaly_detector(speaker=speaker, dash=dash)

            elif "anomaly report" in command:
                speak("Showing anomaly report sir")
                r = get_anomaly_report()
                speak(f"Total {r['total_anomalies']} anomalies detected from {r['total_ips']} IPs sir")

            elif "internet speed" in command:
                speak("Checking internet speed sir")
                d, u = check_internet_speed()
                speak(f"Download speed is {int(d)} Mbps and upload is {int(u)} Mbps")

            elif "my ip" in command:
                speak("Checking your IP address sir")
                try:
                    local_ip = socket.gethostbyname(socket.gethostname())
                    data    = requests.get("http://ip-api.com/json/", timeout=5).json()
                    pub_ip  = data.get("query",   "Unknown")
                    city    = data.get("city",    "Unknown")
                    country = data.get("country", "Unknown")
                    isp     = data.get("isp",     "Unknown")
                    print("[ MY IP INFO ]")
                    print("─" * 35)
                    print(f"  Local IP  : {local_ip}")
                    print(f"  Public IP : {pub_ip}")
                    print(f"  City      : {city}")
                    print(f"  Country   : {country}")
                    print(f"  ISP       : {isp}")
                    print("─" * 35)
                    if dash: dash.set_command(f"IP: {pub_ip}")
                    speak(f"Sir your local IP is {local_ip}. Public IP is {pub_ip}. Location is {city}, {country}. ISP is {isp}.")
                except:
                    speak("Sorry sir, could not fetch IP information")

            elif "check password" in command:
                check_password(None, speaker, dash)

            elif "start deauth monitor" in command:
                speak("Starting WiFi deauth attack monitor sir")
                start_deauth_monitor(speaker, dash)

            elif "stop deauth monitor" in command:
                speak("Stopping WiFi deauth monitor sir")
                stop_deauth_monitor(speaker, dash)

            elif "check mac spoofing" in command:
                if last_devices:
                    speak("Checking MAC spoofing on all devices sir")
                    check_mac_spoofing(last_devices, speaker, dash)
                else:
                    speak("Sir please scan network first then check MAC spoofing")

            elif "check email" in command:
                check_email_breach(speaker, dash)

            elif any(word in command for word in ["exit", "stop", "quit", "bye"]):
                speak("Goodbye sir")
                break

            else:
                speak("Sorry sir command not recognized")

        except:
            continue


# -------- CORE BOOTSTRAP & AUTHENTICATION PROTOCOL --------
dash = start_dashboard()

print("🔐 Starting Secure Authentication...")

pythoncom.CoInitialize()
speak_temp = win32com.client.Dispatch("SAPI.SpVoice")

# --- STEP 1: FACE AUTHENTICATION ---
print("Starting AI Face Recognition...")
face_ok = start_face_auth()

if face_ok:
    # SUCCESS: Direct Access
    print("✅ Welcome back, Sir. Access Granted.")
    speak_temp.Speak("Welcome back Sir. Access granted.")
    threading.Thread(target=jarvis_loop, daemon=True).start()
    while True: time.sleep(1)

else:
    # STEP 2: FACE FAILED -> IMMEDIATELY START VOICE AUTH
    print("❌ Face not recognized. Starting immediate voice verification...")
    speak_temp.Speak("Face not recognized. Please verify your voice sir.")

    voice_ok, msg = verify_voice(speaker=speak_temp)

    if voice_ok:
        # SUCCESS: Voice Access
        print("✅ Voice Verified. Welcome back Sir. Access Granted.")
        speak_temp.Speak("Voice verified. Welcome back Sir. Access granted.")
        threading.Thread(target=jarvis_loop, daemon=True).start()
        while True: time.sleep(1)

    else:
        # STEP 3: BOTH FAILED -> INTRUDER PROTOCOL (PHOTO + FAKE UPDATE)
        print("\n🚨 [ALERT] Unauthorized Access Detected!")
        speak_temp.Speak("Access denied. Intruder detected. Initializing System Core... Please wait.")
        
        # Background mein Photo Click (No delay for intruder)
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, intruder_frame = cap.read()
            if ret:
                # Background thread for saving photo to keep system fast
                threading.Thread(target=security_utils.capture_intruder, args=(intruder_frame,)).start()
            cap.release()

        # Final Security Lockdown
        print("System Lockdown Active. Goodbye.")
        fake_update.start_fake_update()