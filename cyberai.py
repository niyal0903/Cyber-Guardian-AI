import socket
import psutil
import requests
from scapy.all import ARP, Ether, srp
import nmap

class CyberAI:
    def __init__(self):
        print("CYBER AI MODULE READY")

    # 1️⃣ Network Scan
    def scan_network(self):
        print("Scanning Network...")
        # यहाँ सिर्फ placeholder logic, आगे real integration होगा
        print("Network scan complete")

    # 2️⃣ CPU Usage
    def cpu_usage(self):
        print("CPU Usage:", psutil.cpu_percent(), "%")

    # 3️⃣ RAM Usage
    def ram_usage(self):
        print("RAM Usage:", psutil.virtual_memory().percent, "%")

    # 4️⃣ Port Scan
    def port_scan(self, target):
        print(f"Scanning ports on {target}...")
        for port in range(20,1025):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((target, port))
            if result == 0:
                print("Port Open:", port)
            s.close()

    # 5️⃣ Device Finder
    def find_devices(self):
        print("Finding devices in network...")
        # placeholder
        print("Device list shown here")

    # 6️⃣ Public IP
    def ip_info(self):
        try:
            ip = requests.get("https://api.ipify.org").text
            print("Public IP:", ip)
        except:
            print("Unable to fetch IP")