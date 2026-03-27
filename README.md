# 🛡️ Cyber Guardian AI — Mark IV
> **AI-Powered Voice-Controlled Cybersecurity Assistant with Biometric Defense**

Cyber Guardian AI ek next-generation personal security system hai jo sirf threats detect nahi karta — balki **real-time mein respond** bhi karta hai. Tony Stark ke JARVIS se inspired, yeh system aapke WiFi network ka 24/7 guardian hai.

---

## 🆕 Mark IV — What's New?

| Feature | Description |
|:---|:---|
| 🎙️ Voice Authentication | MFCC-based voice biometric — 40 coefficients + Delta features |
| 🤖 ML Anomaly Detection | Isolation Forest model — normal vs abnormal traffic sikhta hai |
| 👥 Evil Twin Detector | Fake WiFi access points detect karta hai |
| 🗺️ Live Attack Map | Folium se real-time attacker locations map pe |
| 🔐 Dual Biometric Gate | Face + Voice — dono fail ho tab intruder system |

---

## 🚀 Core Features

### 🎤 Voice Controlled Interface
Jarvis se seedha baat karo — commands voice se execute hoti hain:

| Command | Action |
|:---|:---|
| `"scan network"` | WiFi devices scan — brand detection + risk analysis |
| `"attack map"` | Live browser map — DDoS attacker locations |
| `"start evil twin"` | Fake AP detector start |
| `"start anomaly"` | ML-based traffic anomaly detection (5 min learning) |
| `"start deauth monitor"` | WiFi deauthentication attack monitor |
| `"check mac spoofing"` | MAC address spoofing detection |
| `"check email"` | Dark web email breach check |
| `"check password"` | Password strength + breach check |
| `"internet speed"` | Real-time download/upload speed test |
| `"my ip"` | Local + public IP, location, ISP info |
| `"anomaly report"` | ML detection report |
| `"evil twin report"` | Evil Twin detection report |

### 🔐 Biometric Authentication System

```
Jarvis Start
    ↓
Face Recognition (DeepFace)
    ↓ Pass → Access Granted ✓
    ↓ Fail ↓
Voice Recognition (MFCC 40-dim)
    ↓ Pass → Access Granted ✓
    ↓ Fail ↓
INTRUDER DETECTED
    → Silent photo capture
    → Acoustic fingerprint
    → Fake Windows Update lockdown
```

### 🤖 ML Anomaly Detection Engine
- **Phase 1 — Learning (5 min):** Normal traffic pattern seekhta hai
- **Phase 2 — Detection (Live):** Isolation Forest model se anomaly score
- **Attack Types Detected:** Port scan, DDoS, ICMP flood, SYN flood, Mass targeting

### 🕵️ Evil Twin AP Detector
- Same SSID ke multiple BSSIDs detect karta hai
- Man-in-the-Middle attack prevention
- Windows `netsh` fallback — monitor mode required nahi

### 📊 Live Iron Man Dashboard
- Animated Jarvis jaw — voice sync ke saath
- Real-time CPU, RAM, Network metrics
- Threat alert — dashboard RED ho jaata hai
- Live command display

### 🛡️ Security Modules
- **DDoS Tracker** — High traffic detect + attacker IP location
- **ARP Spoofing Detector** — MAC-IP mismatch real-time alert
- **MAC Spoof Detector** — Device identity verification
- **WiFi Deauth Monitor** — Kick-off attack detection
- **Password Checker** — Strength analysis + HaveIBeenPwned
- **Email Breach Checker** — Dark web database scan
- **IP Auto Blocker** — Windows Firewall integration
- **Port Scanner** — Fast parallel scan (100 threads)

---

## 🛠️ Tech Stack

| Category | Technologies |
|:---|:---|
| Language | Python 3.10+ |
| AI / ML | DeepFace, TensorFlow, Keras, Isolation Forest |
| Voice Auth | librosa, MFCC, scipy, sounddevice |
| Networking | Scapy, Socket, Requests |
| Visualization | Folium, NetworkX, Matplotlib |
| Voice / Audio | SAPI5 (Win32Com), SpeechRecognition |
| GUI | Tkinter (Iron Man Theme) |
| Geolocation | ip-api.com, Google Maps |

---

## 📂 Project Structure

```
Cyber-Guardian-AI/
├── cyberjarvis.py           ← Main Hub — Voice loop & command routing
├── face_auth.py             ← Biometric face recognition engine
├── voice_auth.py            ← MFCC voice authentication (40-dim)
├── enroll_voice.py          ← Voice enrollment script
├── extract_feature.py       ← Feature extraction from wav
├── evil_twin_detector.py    ← WiFi Evil Twin AP detector
├── ml_anomaly_detector.py   ← Isolation Forest traffic analyzer
├── security_utils.py        ← Silent photo + acoustic detection
├── fake_update.py           ← Intruder deception screen
├── Dashboard.py             ← Iron Man live GUI dashboard
├── ddos_trecker.py          ← DDoS monitoring + attack map
├── mac_spoof_detector.py    ← MAC spoofing detection
├── wifi_deauth_detector.py  ← Deauth attack monitor
├── password_checker.py      ← Password strength + breach check
├── email_breach.py          ← Dark web email checker
├── cyberai.py               ← AI response engine
├── master_voice.wav         ← Owner voice sample
├── master_voice_feat.npy    ← Voice biometric fingerprint
└── requirements.txt         ← All dependencies
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/niyal0903/Cyber-Guardian-AI.git
cd Cyber-Guardian-AI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install deepface tf-keras opencv-python sounddevice scipy
pip install librosa scikit-learn folium speedtest-cli
pip install colorama scapy psutil networkx
```

### 3. Setup Face Authentication
Apni ek clear photo `my_face.jpg` naam se main folder mein rakho.

### 4. Setup Voice Authentication
```bash
python enroll_voice.py
```
3 baar clearly bolo: **"Jarvis activate secure mode"**

### 5. Run as Administrator
```bash
python cyberjarvis.py
```
> ⚠️ Administrator rights zaroori hain — Scapy network scanning ke liye.

---

## 🕵️ Intruder Deception System

Agar face aur voice dono fail ho jaayein:
1. **Silent Photo** — Camera se intruder ki photo capture hoti hai
2. **Acoustic Check** — Room presence detect hota hai  
3. **Fake Windows Update** — Full-screen deception screen activate hoti hai

> 🔑 Secret unlock key: `niyal`

---

## ⚠️ Legal Disclaimer

Yeh tool **sirf educational aur personal network defense** ke liye banaya gaya hai. Apne khud ke network aur devices pe use karein. Kisi aur ke network pe unauthorized use **illegal hai** aur IT Act 2000 ke under punishable hai.

---

## 👨‍💻 Author

**Niyal Patel**  
Cybersecurity & AI Developer  
GitHub: [@niyal0903](https://github.com/niyal0903)

---

 *"Sometimes you gotta run before you can walk." — Tony Stark*