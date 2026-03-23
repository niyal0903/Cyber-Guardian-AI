import threading
import time
import logging
import numpy as np
from collections import defaultdict
from datetime import datetime

# ── ML imports ──
try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("[ML Anomaly] WARNING: scikit-learn not found. Run: pip install scikit-learn")

# ── Logging ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [MLAnomaly] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("MLAnomaly")


# ─────────────────────────────────────────────
#  FEATURE ENGINEERING
#  Har IP ke traffic se 8 features nikalte hain
# ─────────────────────────────────────────────

FEATURE_NAMES = [
    "packets_per_min",    # Kitne packets bheje per minute
    "unique_dst_ports",   # Kitne alag-alag destination ports
    "unique_dst_ips",     # Kitne alag-alag target IPs
    "avg_payload_size",   # Average packet size (bytes)
    "tcp_ratio",          # TCP packets ka ratio (0.0 - 1.0)
    "udp_ratio",          # UDP packets ka ratio
    "icmp_ratio",         # ICMP packets ka ratio (ping flood?)
    "syn_ratio",          # SYN packets ratio (port scan indicator)
]


class IPTracker:
    """
    Ek IP ke traffic statistics track karta hai.
    Rolling window (last 60 seconds) mein features maintain karta hai.
    """
    WINDOW = 60  # seconds

    def __init__(self):
        self.packets     = []          # (timestamp, dst_port, dst_ip, size, proto, flags)
        self.total_bytes = 0

    def add_packet(self, dst_port, dst_ip, size, proto, flags=0):
        now = time.time()
        self.packets.append((now, dst_port, dst_ip, size, proto, flags))
        self.total_bytes += size
        # Old packets remove karo
        cutoff = now - self.WINDOW
        self.packets = [p for p in self.packets if p[0] > cutoff]

    def extract_features(self):
        """8-dimensional feature vector nikalo."""
        if len(self.packets) < 3:
            return None

        now    = time.time()
        window = min(self.WINDOW, now - self.packets[0][0] + 1)

        timestamps, dst_ports, dst_ips, sizes, protos, flags_list = zip(*self.packets)

        n          = len(self.packets)
        ppm        = n / (window / 60)
        udp_ports  = set(dst_ports)
        udp_ips    = set(dst_ips)
        avg_size   = np.mean(sizes) if sizes else 0

        # Protocol ratios
        tcp_count  = sum(1 for p in protos if p == 6)
        udp_count  = sum(1 for p in protos if p == 17)
        icmp_count = sum(1 for p in protos if p == 1)
        syn_count  = sum(1 for f in flags_list if f & 0x02)  # SYN flag

        return [
            ppm,
            len(udp_ports),
            len(udp_ips),
            avg_size,
            tcp_count  / n,
            udp_count  / n,
            icmp_count / n,
            syn_count  / n,
        ]


# ─────────────────────────────────────────────
#  ML MODEL
# ─────────────────────────────────────────────

class AnomalyModel:
    """
    Isolation Forest wrapper with StandardScaler.
    Phase 1: fit() — normal traffic se train karo
    Phase 2: predict() — live traffic score karo
    """

    def __init__(self, contamination=0.05):
        """
        contamination: Expected anomaly fraction (0.05 = 5% anomalies assume karo)
        """
        if not ML_AVAILABLE:
            raise RuntimeError("scikit-learn not installed")

        self.model   = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42,
            n_jobs=-1,
        )
        self.scaler  = StandardScaler()
        self.trained = False
        self.n_train = 0

    def fit(self, feature_matrix):
        """
        feature_matrix: list of 8-dim feature vectors (normal traffic)
        """
        if len(feature_matrix) < 10:
            log.warning(f"Too few samples to train: {len(feature_matrix)}")
            return False

        X = np.array(feature_matrix)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.trained  = True
        self.n_train  = len(X)
        log.info(f"Model trained on {self.n_train} samples")
        return True

    def score(self, feature_vec):
        """
        Returns: (is_anomaly: bool, score: float)
        score < 0 = anomaly, score > 0 = normal
        Isolation Forest: decision_function range roughly -0.5 to 0.5
        """
        if not self.trained:
            return False, 0.0

        X = np.array(feature_vec).reshape(1, -1)
        X_scaled = self.scaler.transform(X)

        score     = self.model.decision_function(X_scaled)[0]
        label     = self.model.predict(X_scaled)[0]
        is_anomaly = (label == -1)

        return is_anomaly, float(score)


# ─────────────────────────────────────────────
#  ALERT SYSTEM
# ─────────────────────────────────────────────

def _classify_anomaly(features):
    """
    Features dekh ke anomaly type guess karo (human-readable reason).
    """
    ppm, ports, ips, size, tcp_r, udp_r, icmp_r, syn_r = features

    reasons = []

    if ppm > 500:
        reasons.append(f"High packet rate ({int(ppm)}/min — possible DDoS)")
    if ports > 50:
        reasons.append(f"Port scanning detected ({int(ports)} unique ports)")
    if ips > 30:
        reasons.append(f"Mass targeting ({int(ips)} unique IPs)")
    if icmp_r > 0.7:
        reasons.append(f"ICMP flood ({int(icmp_r*100)}% ICMP packets)")
    if syn_r > 0.8:
        reasons.append(f"SYN flood / scan ({int(syn_r*100)}% SYN packets)")
    if size > 9000:
        reasons.append(f"Oversized packets ({int(size)} bytes avg)")
    if size < 20 and ppm > 100:
        reasons.append(f"Tiny rapid packets (possible C2 beacon)")

    return reasons if reasons else ["Unusual traffic pattern (ML detected)"]


def _fire_alert(src_ip, features, score, reasons, speaker=None, dash=None, alert_log=None):
    """Alert print karo, voice do, dashboard update karo."""

    timestamp = datetime.now().strftime("%H:%M:%S")

    print("\n" + "═" * 58)
    print("  ⚠  ML ANOMALY DETECTED!")
    print("═" * 58)
    print(f"  Source IP   : {src_ip}")
    print(f"  Time        : {timestamp}")
    print(f"  ML Score    : {score:.4f}  (lower = more suspicious)")
    print(f"  Pkt/min     : {features[0]:.1f}")
    print(f"  Uniq ports  : {int(features[1])}")
    print(f"  Uniq IPs    : {int(features[2])}")
    print(f"  Avg size    : {features[3]:.0f} bytes")
    print(f"\n  Reasons:")
    for r in reasons:
        print(f"    · {r}")
    print("═" * 58 + "\n")

    if alert_log is not None:
        alert_log.append({
            "time"    : timestamp,
            "src_ip"  : src_ip,
            "score"   : score,
            "reasons" : reasons,
            "features": features,
        })

    if speaker:
        try:
            reason_str = reasons[0] if reasons else "unusual pattern"
            speaker.Speak(
                f"Warning sir! Anomaly detected from IP {src_ip}. "
                f"Reason: {reason_str}. ML confidence is high."
            )
        except Exception as e:
            log.error(f"Voice alert failed: {e}")

    if dash:
        try:
            dash.set_command(f"ANOMALY: {src_ip} — {reasons[0][:30]}")
        except:
            pass


# ─────────────────────────────────────────────
#  MAIN DETECTOR CLASS
# ─────────────────────────────────────────────

class MLAnomalyDetector:
    """
    Full pipeline:
      1. Packets capture (scapy)
      2. Per-IP feature extraction (IPTracker)
      3. Learning phase → model train
      4. Detection phase → anomaly scoring + alerts
    """

    LEARN_DURATION  = 300   # 5 min learning (seconds)
    EVAL_INTERVAL   = 10    # Har 10 sec mein evaluate karo
    ALERT_COOLDOWN  = 60    # Same IP ko 60 sec mein ek baar alert

    def __init__(self, speaker=None, dash=None):
        self.speaker    = speaker
        self.dash       = dash
        self.trackers   = defaultdict(IPTracker)
        self.model      = None
        self.alert_log  = []
        self.phase      = "idle"  # idle → learning → detecting
        self._running   = False
        self._lock      = threading.Lock()
        self._last_alert = {}  # ip → timestamp (cooldown)

    # ── Packet Callback ──
    def packet_callback(self, packet):
        try:
            from scapy.all import IP, TCP, UDP, ICMP

            if not packet.haslayer(IP):
                return

            src   = packet[IP].src
            dst   = packet[IP].dst
            size  = len(packet)
            proto = packet[IP].proto
            flags = 0

            dst_port = 0
            if packet.haslayer(TCP):
                dst_port = packet[TCP].dport
                flags    = int(packet[TCP].flags)
            elif packet.haslayer(UDP):
                dst_port = packet[UDP].dport

            with self._lock:
                self.trackers[src].add_packet(dst_port, dst, size, proto, flags)

        except Exception:
            pass

    # ── Learning Phase ──
    def _learning_phase(self):
        self.phase = "learning"
        log.info(f"Learning phase started ({self.LEARN_DURATION}s). Capturing normal traffic...")

        if self.dash:
            try:
                self.dash.set_command("ML Anomaly: LEARNING phase...")
            except:
                pass

        time.sleep(self.LEARN_DURATION)

        # Features collect karo
        feature_matrix = []
        with self._lock:
            for ip, tracker in self.trackers.items():
                fvec = tracker.extract_features()
                if fvec:
                    feature_matrix.append(fvec)

        log.info(f"Learning done. {len(feature_matrix)} IP profiles collected.")

        # Model train karo
        if ML_AVAILABLE and len(feature_matrix) >= 5:
            self.model = AnomalyModel(contamination=0.05)
            success    = self.model.fit(feature_matrix)

            if success:
                self.phase = "detecting"
                msg = f"ML model trained on {len(feature_matrix)} IP profiles. Detection active."
                log.info(msg)
                if self.speaker:
                    self.speaker.Speak(
                        "Machine learning model trained sir. Anomaly detection is now active."
                    )
                if self.dash:
                    try:
                        self.dash.set_command("ML Anomaly: DETECTING")
                    except:
                        pass
            else:
                log.warning("Model training failed — not enough data")
                self.phase = "learning_failed"
        else:
            log.warning("ML not available or not enough data. Using rule-based fallback.")
            self.phase = "rule_based"

    # ── Detection Loop ──
    def _detection_loop(self):
        while self._running and self.phase == "detecting":
            time.sleep(self.EVAL_INTERVAL)

            now = time.time()
            with self._lock:
                ips_to_check = list(self.trackers.keys())

            for src_ip in ips_to_check:
                with self._lock:
                    tracker = self.trackers.get(src_ip)
                    if not tracker:
                        continue
                    fvec = tracker.extract_features()

                if not fvec:
                    continue

                is_anomaly, score = self.model.score(fvec)

                if is_anomaly:
                    # Cooldown check
                    last = self._last_alert.get(src_ip, 0)
                    if now - last < self.ALERT_COOLDOWN:
                        continue

                    self._last_alert[src_ip] = now
                    reasons = _classify_anomaly(fvec)
                    _fire_alert(
                        src_ip, fvec, score, reasons,
                        self.speaker, self.dash, self.alert_log
                    )

    # ── Rule-Based Fallback ──
    def _rule_based_loop(self):
        """Sklearn nahi hai to simple rules use karo."""
        while self._running and self.phase == "rule_based":
            time.sleep(self.EVAL_INTERVAL)
            now = time.time()

            with self._lock:
                ips = list(self.trackers.keys())

            for src_ip in ips:
                with self._lock:
                    tracker = self.trackers.get(src_ip)
                    if not tracker:
                        continue
                    fvec = tracker.extract_features()

                if not fvec:
                    continue

                ppm, ports, ips_count, size, tcp_r, udp_r, icmp_r, syn_r = fvec

                # Rule-based anomaly
                is_anomaly = (
                    ppm > 300 or
                    ports > 30 or
                    ips_count > 20 or
                    icmp_r > 0.7 or
                    syn_r > 0.6
                )

                if is_anomaly:
                    last = self._last_alert.get(src_ip, 0)
                    if now - last < self.ALERT_COOLDOWN:
                        continue

                    self._last_alert[src_ip] = now
                    reasons = _classify_anomaly(fvec)
                    _fire_alert(
                        src_ip, fvec, -1.0, reasons,
                        self.speaker, self.dash, self.alert_log
                    )

    # ── Main Run Loop ──
    def _run(self):
        from scapy.all import sniff

        # Start packet capture in background
        sniff_thread = threading.Thread(
            target=lambda: sniff(
                prn=self.packet_callback,
                store=False,
                stop_filter=lambda p: not self._running,
            ),
            daemon=True
        )
        sniff_thread.start()

        # Learning phase
        self._learning_phase()

        # Detection / fallback loop
        if self.phase == "detecting":
            self._detection_loop()
        elif self.phase == "rule_based":
            self._rule_based_loop()

    def start(self):
        if self._running:
            log.warning("Detector already running")
            return

        self._running = True
        t = threading.Thread(target=self._run, daemon=True, name="MLAnomalyDetector")
        t.start()
        log.info("ML Anomaly Detector started")

    def stop(self):
        self._running = False
        self.phase    = "idle"
        log.info(f"Stopped. Total anomalies detected: {len(self.alert_log)}")

    def get_summary(self):
        return {
            "phase"         : self.phase,
            "total_ips"     : len(self.trackers),
            "total_anomalies": len(self.alert_log),
            "events"        : self.alert_log.copy(),
        }

    def print_report(self):
        s = self.get_summary()
        print("\n" + "═" * 58)
        print("  ML ANOMALY DETECTION REPORT")
        print("═" * 58)
        print(f"  Phase            : {s['phase']}")
        print(f"  IPs monitored    : {s['total_ips']}")
        print(f"  Anomalies found  : {s['total_anomalies']}")
        if s["events"]:
            print("\n  Events:")
            for ev in s["events"]:
                print(f"\n  [{ev['time']}] {ev['src_ip']}")
                print(f"    Score  : {ev['score']:.4f}")
                for r in ev["reasons"]:
                    print(f"    · {r}")
        print("═" * 58 + "\n")


# ─────────────────────────────────────────────
#  GLOBAL INSTANCE (Jarvis ke liye)
# ─────────────────────────────────────────────

_detector_instance = None


def start_anomaly_detector(speaker=None, dash=None):
    global _detector_instance

    if _detector_instance and _detector_instance._running:
        log.warning("Already running")
        if speaker:
            speaker.Speak("Anomaly detector is already running sir")
        return

    _detector_instance = MLAnomalyDetector(speaker=speaker, dash=dash)
    _detector_instance.start()

    msg = (
        "ML Anomaly Detector started sir. "
        "Learning normal traffic for 5 minutes. "
        "After that, real-time detection will begin."
    )
    log.info(msg)
    if speaker:
        speaker.Speak(msg)


def stop_anomaly_detector(speaker=None, dash=None):
    global _detector_instance

    if not _detector_instance:
        return

    _detector_instance.stop()
    _detector_instance.print_report()

    n = len(_detector_instance.alert_log)
    if speaker:
        speaker.Speak(
            f"Anomaly detector stopped sir. "
            f"{n} anomalies were detected in this session."
        )


def get_anomaly_report():
    if _detector_instance:
        return _detector_instance.get_summary()
    return {"phase": "idle", "total_ips": 0, "total_anomalies": 0, "events": []}


# ─────────────────────────────────────────────
#  JARVIS COMMAND INTEGRATION
# ─────────────────────────────────────────────
"""
main.py mein yeh commands add karo jarvis_loop ke andar:

    elif "start anomaly detection" in command or "start ml detection" in command:
        speak("Starting ML anomaly detection sir. Learning phase will take 5 minutes.")
        start_anomaly_detector(speaker=speaker, dash=dash)

    elif "stop anomaly detection" in command:
        speak("Stopping anomaly detection sir")
        stop_anomaly_detector(speaker=speaker, dash=dash)

    elif "anomaly report" in command:
        speak("Showing anomaly detection report sir")
        if _detector_instance:
            _detector_instance.print_report()
"""


# ─────────────────────────────────────────────
#  STANDALONE TEST (no real network needed)
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("ML Anomaly Detector — Simulation Test")
    print("(No real network capture — injecting fake data)\n")

    if not ML_AVAILABLE:
        print("ERROR: pip install scikit-learn numpy")
        exit(1)

    # Simulate normal traffic
    normal_features = []
    for _ in range(50):
        normal_features.append([
            np.random.uniform(10, 80),    # ppm — low/normal
            np.random.randint(1, 10),     # few ports
            np.random.randint(1, 5),      # few IPs
            np.random.uniform(200, 1400), # normal size
            np.random.uniform(0.6, 0.9),  # mostly TCP
            np.random.uniform(0.05, 0.3), # some UDP
            np.random.uniform(0, 0.05),   # almost no ICMP
            np.random.uniform(0, 0.1),    # few SYNs
        ])

    # Train model
    model = AnomalyModel(contamination=0.05)
    model.fit(normal_features)

    print("Model trained on 50 normal traffic samples.\n")
    print("Testing anomalies:\n")

    # Test 1: Port scan
    scan_features = [800, 200, 5, 60, 0.95, 0.02, 0.0, 0.9]
    is_anom, score = model.score(scan_features)
    reasons = _classify_anomaly(scan_features)
    print(f"Port scan test  → Anomaly: {is_anom}, Score: {score:.4f}")
    print(f"  Reasons: {reasons}\n")

    # Test 2: Normal
    norm_features = [30, 3, 2, 800, 0.75, 0.2, 0.01, 0.05]
    is_anom, score = model.score(norm_features)
    print(f"Normal traffic  → Anomaly: {is_anom}, Score: {score:.4f}\n")

    # Test 3: ICMP flood
    icmp_features = [600, 1, 100, 40, 0.0, 0.0, 0.98, 0.0]
    is_anom, score = model.score(icmp_features)
    reasons = _classify_anomaly(icmp_features)
    print(f"ICMP flood test → Anomaly: {is_anom}, Score: {score:.4f}")
    print(f"  Reasons: {reasons}\n")

    print("Test complete!")