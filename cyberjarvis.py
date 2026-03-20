
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

# -------- MAC Vendor Lookup --------
def get_vendor(mac):
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        return "Unknown Vendor"
    except:
        return "Unknown Vendor"

# -------- Device Brand Detection --------
def detect_brand(vendor):
    vendor = vendor.lower()
    if "samsung" in vendor:
        return "Samsung Phone"
    elif "apple" in vendor:
        return "iPhone / Apple Device"
    elif "xiaomi" in vendor or "redmi" in vendor:
        return "Xiaomi Phone"
    elif "oppo" in vendor:
        return "Oppo Phone"
    elif "vivo" in vendor:
        return "Vivo Phone"
    elif "realme" in vendor:
        return "Realme Phone"
    elif "amazon" in vendor:
        return "Alexa / Fire TV"
    elif "intel" in vendor:
        return "Laptop / PC"
    elif "huawei" in vendor:
        return "Huawei Device"
    else:
        return "Unknown Device"

# -------- WiFi Scan --------
def scan_wifi_devices():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    parts    = local_ip.split(".")
    subnet   = parts[0] + "." + parts[1] + "." + parts[2] + ".0/24"
    print("Scanning subnet:", subnet)

    arp    = ARP(pdst=subnet)
    ether  = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result  = srp(packet, timeout=3, verbose=0)[0]
    devices = []

    for sent, received in result:
        ip  = received.psrc
        mac = received.hwsrc
        try:
            name = socket.gethostbyaddr(ip)[0]
        except:
            name = "Unknown"

        vendor = get_vendor(mac)
        devices.append((ip, mac, name, vendor))

    return devices

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
        print("Device:", brand, "| IP:", ip)

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

# -------- speaker global — ddos_tracker ke liye --------
speaker = None

# -------- Voice Loop --------
def jarvis_loop():

    global speaker
    pythoncom.CoInitialize()
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    cyber   = CyberAI()

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
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            command = recognizer.recognize_google(audio, language="en-IN").lower().strip()
            print("You said:", command)

            if dash: dash.set_command(command)

            # -------- JARVIS WAKE WORD --------
            if "jarvis" in command and len(command.split()) == 1:
                speak("Yes sir")

            elif "system status" in command:
                speak("Checking system status sir")
                cyber.cpu_usage()
                cyber.ram_usage()
                speak("System status done sir")

            elif "scan network" in command:
                speak("Scanning network sir")
                devices = scan_wifi_devices()

                if dash:
                    dev_list = []
                    for ip, mac, name, vendor in devices:
                        brand  = detect_brand(vendor)
                        status = "RISK" if brand == "Unknown Device" else "OK"
                        dev_list.append({"name": brand, "ip": ip, "status": status})
                    dash.set_devices(dev_list)

                risk = network_map(devices)
                intrusion_detection(devices)

                speak("Scanning ports sir please wait")
                for ip, mac, name, vendor in devices:
                    port_scan(ip)

                threat = ai_threat_prediction(devices)

                if dash:
                    dash.set_threat(threat.upper())
                    if threat == "High":
                        dash.set_mode("alert")

                soc_dashboard(devices, threat)

                speak(f"Network risk level is {risk} sir")
                network_graph(devices)
                speak("Network graph is ready sir")

            elif "packet sniffer" in command:
                speak("Starting packet sniffer sir")
                start_sniffer()
                speak("Sniffer stopped sir")

            elif "show attackers" in command:
                speak("Showing all tracked attackers sir")
                show_all_attackers()
                speak("Attacker report done sir")

            elif "check password" in command:
                speak("Tell me the password sir")
                try:
                    with mic as source:
                        audio_pwd = recognizer.listen(source, timeout=8, phrase_time_limit=6)
                    pwd = recognizer.recognize_google(audio_pwd).strip()
                    print("Password received:", pwd)
                    check_password(pwd, speaker, dash)
                except:
                    speak("Sorry sir, could not hear the password")

            elif any(word in command for word in ["exit", "stop", "quit", "bye"]):
                speak("Goodbye sir")
                break

            else:
                speak("Sorry sir command not recognized")

        except:
            continue

dash = start_dashboard()

voice_thread        = threading.Thread(target=jarvis_loop)
voice_thread.daemon = True
voice_thread.start()

while True:
    pass