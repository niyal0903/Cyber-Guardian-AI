import tkinter as tk
import math
import time
import random
import threading
import psutil

# ── Colors ───────────────────────────────────────────────────
BG      = "#000000"
CYAN    = "#00d4ff"
CYAN2   = "#007a9a"
GREEN   = "#00ff88"
RED     = "#ff3030"
YELLOW  = "#ffcc00"
ORANGE  = "#ff8c00"
WHITE   = "#c8f4ff"
PANEL   = "#030b13"
BORDER  = "#061c2c"
DIM     = "#0b2e40"


class JarvisDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS // CYBER AI v4.0")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ── State ────────────────────────────────────────────
        self.mode      = "idle"   # idle | speaking | listening | alert
        self.cpu       = 0
        self.ram       = 0
        self.threat    = "LOW"
        self.packets   = 0
        self.down_mb   = 0.0
        self.up_mb     = 0.0
        self.devices   = []
        self.ddos_list = []
        self.command   = ""

        # ── Animation vars ───────────────────────────────────
        self._frame      = 0
        self._eye_glow   = 0.5
        self._eye_dir    = 1
        self._jaw_open   = 0.0
        self._jaw_target = 0.0
        self._hud_phase  = 0.0
        self._scan_y     = 0
        self._breathe    = 0.0
        self._arc_phase  = 0.0
        self._blink_open = True
        self._blink_t    = 0
        self._shake_x    = 0
        self._shake_y    = 0
        self._shake_t    = 0
        self._rep_flash  = 0.0
        self._traffic    = [28] * 120
        self._blink_dot  = True
        self._lock       = threading.Lock()

        self._build_ui()
        self._animate()

    # ─────────────────────────────────────────────────────────
    # PUBLIC API — cyberjarvis.py yeh call karega
    # ─────────────────────────────────────────────────────────
    def set_mode(self, mode):
        """idle | speaking | listening | alert"""
        with self._lock:
            self.mode = mode
            if mode == "alert":
                self._shake_t  = 40
                self._rep_flash = 1.0

    def set_devices(self, devices):
        """
        devices = [
            {"name": "Samsung", "ip": "192.168.1.2", "status": "OK"},
            {"name": "Unknown", "ip": "192.168.1.8", "status": "RISK"},
        ]
        """
        with self._lock:
            self.devices = devices

    def add_ddos(self, ip, city, country, packets):
        with self._lock:
            self.ddos_list.append({
                "ip": ip, "city": city,
                "country": country, "packets": packets
            })
            if len(self.ddos_list) > 4:
                self.ddos_list = self.ddos_list[-4:]
            self.mode    = "alert"
            self._shake_t = 45
            self._rep_flash = 1.0

    def set_threat(self, level):
        with self._lock:
            self.threat = level

    def set_packets(self, n):
        with self._lock:
            self.packets = n

    def set_bandwidth(self, down_mb, up_mb):
        with self._lock:
            self.down_mb = round(down_mb, 1)
            self.up_mb   = round(up_mb,   1)

    def set_command(self, cmd):
        with self._lock:
            self.command = cmd

    def traffic_spike(self):
        with self._lock:
            for _ in range(40):
                self._traffic.append(65 + random.randint(0, 30))
            self._traffic = self._traffic[-120:]

    # ─────────────────────────────────────────────────────────
    # BUILD UI
    # ─────────────────────────────────────────────────────────
    def _build_ui(self):
        W = 900

        # ── HEADER ───────────────────────────────────────────
        hdr = tk.Frame(self.root, bg=BG)
        hdr.pack(fill="x", padx=8, pady=(6, 3))

        tk.Label(hdr, text="JAR", bg=BG, fg=CYAN,
                 font=("Courier", 14, "bold")).pack(side="left")
        tk.Label(hdr, text="VIS", bg=BG, fg=RED,
                 font=("Courier", 14, "bold")).pack(side="left")
        tk.Label(hdr, text="  // CYBER AI v4.0 — MARK L — LIVE DASHBOARD",
                 bg=BG, fg=DIM, font=("Courier", 8)).pack(side="left")

        self._lbl_time = tk.Label(hdr, text="", bg=BG, fg=CYAN2,
                                  font=("Courier", 8))
        self._lbl_time.pack(side="right")
        self._lbl_online = tk.Label(hdr, text="● ONLINE", bg=BG, fg=GREEN,
                                    font=("Courier", 8))
        self._lbl_online.pack(side="right", padx=10)

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=8)

        # ── MODE BAR ─────────────────────────────────────────
        mode_f = tk.Frame(self.root, bg=BG)
        mode_f.pack(fill="x", padx=8, pady=3)
        tk.Label(mode_f, text="STATUS: ", bg=BG, fg=DIM,
                 font=("Courier", 8)).pack(side="left")
        self._lbl_mode = tk.Label(mode_f, text="STANDBY", bg=BG, fg=YELLOW,
                                  font=("Courier", 9, "bold"))
        self._lbl_mode.pack(side="left")

        # ── MAIN GRID ────────────────────────────────────────
        mid = tk.Frame(self.root, bg=BG)
        mid.pack(fill="x", padx=8, pady=4)

        # Left column
        left = tk.Frame(mid, bg=BG, width=165)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)
        self._build_left(left)

        # Center — Iron Man Face canvas
        self._face_canvas = tk.Canvas(mid, width=380, height=450,
                                      bg=BG, highlightthickness=0)
        self._face_canvas.pack(side="left", padx=6)

        # Right column
        right = tk.Frame(mid, bg=BG, width=165)
        right.pack(side="left", fill="y")
        right.pack_propagate(False)
        self._build_right(right)

        # ── TRAFFIC ──────────────────────────────────────────
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=8, pady=2)
        tp_f = tk.Frame(self.root, bg=PANEL)
        tp_f.pack(fill="x", padx=8, pady=3)
        tk.Label(tp_f, text="// LIVE NETWORK TRAFFIC",
                 bg=PANEL, fg=DIM, font=("Courier", 7)).pack(anchor="w", padx=6, pady=(4, 2))
        self._traffic_canvas = tk.Canvas(tp_f, width=880, height=55,
                                         bg=PANEL, highlightthickness=0)
        self._traffic_canvas.pack(padx=6, pady=(0, 6))

        # ── BUTTONS ──────────────────────────────────────────
        btn_f = tk.Frame(self.root, bg=BG)
        btn_f.pack(pady=(2, 8), padx=8, anchor="w")
        for txt, cmd in [
            ("IDLE",            lambda: self.set_mode("idle")),
            ("JARVIS SPEAKING", lambda: self.set_mode("speaking")),
            ("USER SPEAKING",   lambda: self.set_mode("listening")),
            ("SIMULATE DDOS",   self._sim_ddos),
            ("TRAFFIC SPIKE",   self.traffic_spike),
            ("SCAN ANIM",       self._scan_anim),
        ]:
            b = tk.Button(btn_f, text=txt, bg=BG, fg=CYAN2,
                          activebackground=CYAN, activeforeground=BG,
                          font=("Courier", 8), relief="solid", bd=1,
                          padx=8, pady=4, command=cmd)
            b.pack(side="left", padx=3)
            b.bind("<Enter>", lambda e, w=b: w.config(bg=CYAN, fg=BG))
            b.bind("<Leave>", lambda e, w=b: w.config(bg=BG, fg=CYAN2))

    def _panel(self, parent, title):
        f = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER,
                     highlightthickness=1)
        f.pack(fill="x", pady=(0, 5), ipadx=5, ipady=5)
        tk.Label(f, text=title, bg=PANEL, fg=DIM,
                 font=("Courier", 7)).pack(anchor="w", padx=6, pady=(3, 2))
        return f

    def _build_left(self, parent):
        # System stats
        sf = self._panel(parent, "// SYSTEM")
        grid = tk.Frame(sf, bg=PANEL)
        grid.pack(fill="x", padx=5, pady=2)
        self._stat_labels = {}
        items = [("CPU", GREEN), ("RAM", CYAN), ("THREAT", YELLOW), ("PKTS", WHITE)]
        for i, (k, c) in enumerate(items):
            col = i % 2
            row = i // 2
            box = tk.Frame(grid, bg="#020810", bd=1, relief="solid")
            box.grid(row=row, column=col, padx=2, pady=2, ipadx=6, ipady=4)
            tk.Label(box, text=k, bg="#020810", fg=DIM,
                     font=("Courier", 6)).pack()
            lbl = tk.Label(box, text="--", bg="#020810", fg=c,
                           font=("Courier", 12, "bold"))
            lbl.pack()
            self._stat_labels[k] = lbl

        # CPU/RAM bars
        bf = tk.Frame(sf, bg=PANEL)
        bf.pack(fill="x", padx=6, pady=(2, 0))
        self._bars = {}
        for label, color, key in [("CPU", GREEN, "cpu"), ("RAM", CYAN, "ram"), ("PWR", ORANGE, "pwr")]:
            row = tk.Frame(bf, bg=PANEL)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=f"{label}", bg=PANEL, fg=DIM,
                     font=("Courier", 7), width=4, anchor="w").pack(side="left")
            bar_bg = tk.Frame(row, bg=BORDER, height=4, width=110)
            bar_bg.pack(side="left", padx=3)
            bar_bg.pack_propagate(False)
            bar_fill = tk.Frame(bar_bg, bg=color, height=4, width=0)
            bar_fill.place(x=0, y=0, relheight=1)
            val_lbl = tk.Label(row, text="--", bg=PANEL, fg=DIM,
                               font=("Courier", 7), width=5)
            val_lbl.pack(side="left")
            self._bars[key] = (bar_bg, bar_fill, val_lbl, color)

        # Devices
        df = self._panel(parent, "// NETWORK DEVICES")
        self._dev_frame = df

        # Bandwidth
        bwf = self._panel(parent, "// BANDWIDTH")
        self._bw_bars = {}
        for label, color, key in [("DOWN", CYAN, "down"), ("UP", GREEN, "up"), ("PKTS", YELLOW, "pkts")]:
            row = tk.Frame(bwf, bg=PANEL)
            row.pack(fill="x", padx=6, pady=1)
            tk.Label(row, text=label, bg=PANEL, fg=DIM,
                     font=("Courier", 7), width=4, anchor="w").pack(side="left")
            bar_bg = tk.Frame(row, bg=BORDER, height=4, width=90)
            bar_bg.pack(side="left", padx=3)
            bar_bg.pack_propagate(False)
            bar_fill = tk.Frame(bar_bg, bg=color, height=4, width=0)
            bar_fill.place(x=0, y=0, relheight=1)
            val_lbl = tk.Label(row, text="--", bg=PANEL, fg=DIM,
                               font=("Courier", 7), width=7)
            val_lbl.pack(side="left")
            self._bw_bars[key] = (bar_bg, bar_fill, val_lbl)

    def _build_right(self, parent):
        # Arc reactor canvas
        af = self._panel(parent, "// ARC REACTOR")
        self._arc_canvas = tk.Canvas(af, width=150, height=80,
                                     bg=PANEL, highlightthickness=0)
        self._arc_canvas.pack(padx=5, pady=3)

        # DDoS
        df = self._panel(parent, "// DDOS ALERTS")
        self._ddos_frame = df

        # Commands
        cf = self._panel(parent, "// VOICE COMMANDS")
        for cmd in ["• jarvis", "• scan network", "• packet sniffer",
                    "• system status", "• show attackers", "• exit / bye"]:
            tk.Label(cf, text=cmd, bg=PANEL, fg=CYAN2,
                     font=("Courier", 7)).pack(anchor="w", padx=8)

        # Last command
        lf = self._panel(parent, "// LAST COMMAND")
        self._lbl_cmd = tk.Label(lf, text="--", bg=PANEL, fg=CYAN,
                                 font=("Courier", 8), wraplength=140)
        self._lbl_cmd.pack(anchor="w", padx=6)

    # ─────────────────────────────────────────────────────────
    # ANIMATION LOOP
    # ─────────────────────────────────────────────────────────
    def _animate(self):
        self._frame += 1
        self._breathe  += 0.018
        self._hud_phase += 0.04
        self._arc_phase += 0.055
        self._scan_y    = (self._scan_y + 2) % 450

        # Blink dot
        if self._frame % 30 == 0:
            self._blink_dot = not self._blink_dot
            self._lbl_online.config(fg=GREEN if self._blink_dot else BG)

        # Clock
        self._lbl_time.config(text=time.strftime("%H:%M:%S"))

        # Eye blink
        self._blink_t += 1
        if self._blink_t > 200 + random.randint(0, 120):
            self._blink_open = False
            self._blink_t = 0
        if not self._blink_open and self._blink_t > 8:
            self._blink_open = True

        # Shake
        if self._shake_t > 0:
            self._shake_x = random.uniform(-7, 7)
            self._shake_y = random.uniform(-3, 3)
            self._shake_t -= 1
        else:
            self._shake_x = 0
            self._shake_y = 0

        # Repulsor flash fade
        if self._rep_flash > 0:
            self._rep_flash = max(0, self._rep_flash - 0.04)

        # Eye glow
        if self.mode == "speaking":
            self._eye_glow += self._eye_dir * 0.055
            if self._eye_glow >= 1.0:
                self._eye_glow = 1.0; self._eye_dir = -1
            if self._eye_glow <= 0.3:
                self._eye_glow = 0.3; self._eye_dir = 1
        elif self.mode == "alert":
            self._eye_glow = 0.85 + 0.15 * math.sin(self._frame * 0.22)
        else:
            self._eye_glow = 0.4 + 0.12 * math.sin(self._breathe * 0.5)

        # Jaw
        if self.mode == "speaking":
            self._jaw_target = 0.28 + 0.72 * abs(math.sin(self._frame * 0.17))
        elif self.mode == "alert":
            self._jaw_target = 0.06
        else:
            self._jaw_target = 0.0
        self._jaw_open += (self._jaw_target - self._jaw_open) * 0.13

        # Auto system stats
        if self._frame % 40 == 0:
            self.cpu = psutil.cpu_percent(interval=0)
            self.ram = psutil.virtual_memory().percent
            self.packets = max(50, self.packets + random.randint(-8, 8))
            self.down_mb = round(max(0.1, self.down_mb + random.uniform(-0.15, 0.15)), 1)
            self.up_mb   = round(max(0.1, self.up_mb   + random.uniform(-0.08, 0.08)), 1)

        # Traffic
        self._traffic = self._traffic[1:] + [28 + random.randint(-15, 15)]

        # Update all UI
        self._update_stats()
        self._update_devices()
        self._update_ddos()
        self._draw_face()
        self._draw_arc()
        self._draw_traffic()

        self.root.after(40, self._animate)  # ~25fps

    # ─────────────────────────────────────────────────────────
    # UPDATE STATS
    # ─────────────────────────────────────────────────────────
    def _update_stats(self):
        # Mode label
        modes = {
            "idle":      ("STANDBY",          YELLOW),
            "speaking":  ("JARVIS SPEAKING",   CYAN),
            "listening": ("USER SPEAKING",     GREEN),
            "alert":     ("THREAT DETECTED!",  RED),
        }
        txt, col = modes.get(self.mode, ("STANDBY", YELLOW))
        self._lbl_mode.config(text=txt, fg=col)

        # Stat boxes
        cpu_col = RED if self.cpu > 80 else (YELLOW if self.cpu > 60 else GREEN)
        thr_col = RED if self.threat == "HIGH" else (YELLOW if self.threat == "MEDIUM" else GREEN)
        self._stat_labels["CPU"].config(text=f"{int(self.cpu)}%", fg=cpu_col)
        self._stat_labels["RAM"].config(text=f"{int(self.ram)}%")
        self._stat_labels["THREAT"].config(text=self.threat, fg=thr_col)
        self._stat_labels["PKTS"].config(text=str(self.packets))

        # Bars
        for key, val, color in [
            ("cpu",  self.cpu / 100,     GREEN if self.cpu < 60 else (YELLOW if self.cpu < 80 else RED)),
            ("ram",  self.ram / 100,     CYAN),
            ("pwr",  0.87,               ORANGE),
        ]:
            bg, fill, lbl, _ = self._bars[key]
            w = int(bg.winfo_width() * min(val, 1.0))
            fill.place(x=0, y=0, width=max(0, w), relheight=1)
            fill.config(bg=color)
            lbl.config(text=f"{int(val*100)}%")

        # Bandwidth bars
        for key, val, max_val, txt in [
            ("down",  self.down_mb,  10,  f"{self.down_mb:.1f}MB"),
            ("up",    self.up_mb,    5,   f"{self.up_mb:.1f}MB"),
            ("pkts",  self.packets,  300, f"{self.packets}/s"),
        ]:
            bg, fill, lbl = self._bw_bars[key]
            w = int(bg.winfo_width() * min(val / max_val, 1.0))
            fill.place(x=0, y=0, width=max(0, w), relheight=1)
            lbl.config(text=txt)

        # Last command
        if self.command:
            self._lbl_cmd.config(text=f'"{self.command}"')

    def _update_devices(self):
        # Clear old device rows (keep panel title)
        for w in self._dev_frame.winfo_children():
            if isinstance(w, tk.Frame):
                w.destroy()

        if not self.devices:
            tk.Label(self._dev_frame, text="No devices",
                     bg=PANEL, fg=DIM, font=("Courier", 7)).pack(padx=6)
            return

        for dev in self.devices[:7]:
            row = tk.Frame(self._dev_frame, bg=PANEL)
            row.pack(fill="x", padx=6, pady=1)
            col = GREEN if dev.get("status") == "OK" else (YELLOW if dev.get("status") == "WARN" else RED)
            tk.Label(row, text="●", bg=PANEL, fg=col,
                     font=("Courier", 7)).pack(side="left")
            info = tk.Frame(row, bg=PANEL)
            info.pack(side="left", padx=4, fill="x", expand=True)
            tk.Label(info, text=dev.get("name", "?"), bg=PANEL, fg=WHITE,
                     font=("Courier", 8)).pack(anchor="w")
            tk.Label(info, text=dev.get("ip", "?"), bg=PANEL, fg=DIM,
                     font=("Courier", 7)).pack(anchor="w")
            tk.Label(row, text=dev.get("status", "?"), bg=PANEL, fg=col,
                     font=("Courier", 7)).pack(side="right")

    def _update_ddos(self):
        for w in self._ddos_frame.winfo_children():
            if isinstance(w, tk.Frame):
                w.destroy()

        if not self.ddos_list:
            tk.Label(self._ddos_frame, text="No attacks",
                     bg=PANEL, fg=DIM, font=("Courier", 7)).pack(padx=6, pady=4)
            return

        for atk in self.ddos_list[-3:]:
            box = tk.Frame(self._ddos_frame, bg="#0c0405",
                           highlightbackground="#220507", highlightthickness=1)
            box.pack(fill="x", padx=5, pady=2, ipadx=4, ipady=3)
            tk.Label(box, text=f"⚠ {atk['ip']}", bg="#0c0405", fg=RED,
                     font=("Courier", 8, "bold")).pack(anchor="w")
            tk.Label(box, text=f"{atk['city']}, {atk['country']}", bg="#0c0405", fg=DIM,
                     font=("Courier", 7)).pack(anchor="w")
            tk.Label(box, text=f"Pkts: {atk['packets']} — BLOCKED", bg="#0c0405", fg=YELLOW,
                     font=("Courier", 7)).pack(anchor="w")

    # ─────────────────────────────────────────────────────────
    # DRAW IRON MAN FACE
    # ─────────────────────────────────────────────────────────
    def _draw_face(self):
        c  = self._face_canvas
        c.delete("dynamic")

        W, H   = 380, 450
        is_a   = self.mode == "alert"
        is_s   = self.mode == "speaking"
        eye_g  = self._eye_glow
        jaw_o  = self._jaw_open
        sx, sy = self._shake_x, self._shake_y

        fcx = W // 2 + sx
        fcy = H // 2 + sy + 18

        # HUD scan line
        c.create_rectangle(0, self._scan_y - 1, W, self._scan_y + 2,
                           fill="#001a28", outline="", tags="dynamic")

        # Corner brackets
        for x, y, sx2, sy2 in [(10,8,1,1),(W-10,8,-1,1),(10,H-8,1,-1),(W-10,H-8,-1,-1)]:
            c.create_line(x, y+sy2*12, x, y, x+sx2*12, y,
                         fill=CYAN2, width=1, tags="dynamic")

        # Repulsor flash
        if self._rep_flash > 0:
            alpha_col = self._hex_alpha("#001525", self._rep_flash * 0.4)
            c.create_rectangle(0, 0, W, H, fill="#001525" if not is_a else "#280606",
                               stipple="gray25", outline="", tags="dynamic")

        # Neck base
        self._oval_path(c, fcx, fcy+190, 60, 25, fill="#090f18", outline=CYAN2, width=1)
        for s in [-1, 1]:
            pts = [fcx+s*22,fcy+190, fcx+s*57,fcy+196, fcx+s*60,fcy+218, fcx+s*32,fcy+233, fcx+s*12,fcy+229]
            c.create_polygon(pts, fill="#0b1720", outline=CYAN2, width=1, tags="dynamic")

        # Main helmet dome
        dome_pts = [
            fcx-90,fcy-148, fcx-55,fcy-193, fcx,fcy-195,
            fcx+55,fcy-193, fcx+90,fcy-148, fcx+116,fcy-108,
            fcx+122,fcy-52, fcx+108,fcy-4, fcx+100,fcy+46,
            fcx+84,fcy+97, fcx+62,fcy+142, fcx+40,fcy+178,
            fcx+20,fcy+195, fcx,fcy+200,
            fcx-20,fcy+195, fcx-40,fcy+178,
            fcx-62,fcy+142, fcx-84,fcy+97,
            fcx-100,fcy+46, fcx-108,fcy-4,
            fcx-122,fcy-52, fcx-116,fcy-108,
        ]
        outline_col = "#ff2a0a" if is_a else CYAN
        c.create_polygon(dome_pts, fill="#0f1e2c", outline=outline_col,
                        width=2, smooth=True, tags="dynamic")

        # Forehead plate
        fp = [fcx-46,fcy-150, fcx-26,fcy-193, fcx,fcy-195,
              fcx+26,fcy-193, fcx+46,fcy-150, fcx+64,fcy-108,
              fcx,fcy-98, fcx-64,fcy-108]
        c.create_polygon(fp, fill="#142838", outline=CYAN, width=1, tags="dynamic")

        # Temple plates
        for s in [-1, 1]:
            tp = [fcx+s*64,fcy-108, fcx+s*90,fcy-148, fcx+s*116,fcy-108,
                  fcx+s*108,fcy-4, fcx+s*84,fcy+8, fcx+s*64,fcy-56]
            c.create_polygon(tp, fill="#0f1f30", outline=CYAN, width=1, tags="dynamic")
            # Hex bolt
            tbx, tby = fcx+s*98, fcy-70
            self._hex_shape(c, tbx, tby, 7, "#1a3a58", CYAN, tags="dynamic")
            c.create_oval(tbx-2.5,tby-2.5,tbx+2.5,tby+2.5, fill=CYAN, outline="", tags="dynamic")
            # Lower temple
            lt = [fcx+s*64,fcy-56, fcx+s*84,fcy+8, fcx+s*80,fcy+70,
                  fcx+s*62,fcy+84, fcx+s*50,fcy+66, fcx+s*56,fcy-28]
            c.create_polygon(lt, fill="#0d1c2c", outline=CYAN2, width=1, tags="dynamic")

        # Cheeks
        for s in [-1, 1]:
            ck = [fcx+s*22,fcy-56, fcx+s*56,fcy-28, fcx+s*78,fcy+32,
                  fcx+s*72,fcy+92, fcx+s*50,fcy+120, fcx+s*22,fcy+76]
            c.create_polygon(ck, fill="#0c1c2c", outline=CYAN2, width=1, tags="dynamic")

        # Brow ridges
        eye_y = fcy - 72
        for s in [-1, 1]:
            ex = fcx + s*47
            br = [ex-s*36,eye_y-26, ex+s*14,eye_y-32, ex+s*36,eye_y-22,
                  ex+s*32,eye_y-12, ex+s*20,eye_y-9, ex-s*8,eye_y-7]
            c.create_polygon(br, fill="#102540", outline=CYAN, width=1, tags="dynamic")

        # Eyes
        eye_col  = f"#{self._lerp_color('ff3010', '00d4ff', 1-eye_g if is_a else 0)}" if is_a else CYAN
        eye_col2 = self._rgba_color(CYAN, eye_g) if not is_a else self._rgba_color("#ff3010", eye_g)

        for s in [-1, 1]:
            ex = fcx + s*47
            # Socket
            sk = [ex-30,eye_y-8, ex-20,eye_y-18, ex+20,eye_y-18, ex+30,eye_y-8,
                  ex+26,eye_y+11, ex+14,eye_y+20, ex-14,eye_y+20, ex-26,eye_y+11]
            c.create_polygon(sk, fill="#010508", outline=outline_col, width=2, tags="dynamic")

            if self._blink_open:
                # Inner glow fill
                gf = [ex-22,eye_y-4, ex-14,eye_y-13, ex+14,eye_y-13, ex+22,eye_y-4,
                      ex+18,eye_y+9, ex-18,eye_y+9]
                c.create_polygon(gf, fill=eye_col2, outline="", tags="dynamic")

                # Bright scan line
                bright = "#ffa060" if is_a else WHITE
                c.create_line(ex-20,eye_y, ex+20,eye_y, fill=bright, width=2, tags="dynamic")

                # Hot core oval
                c.create_oval(ex-10,eye_y-5, ex+10,eye_y+5,
                             fill=bright, outline="", tags="dynamic")

                # Outer glow (simulated with big oval)
                glow_col = "#ff3010" if is_a else CYAN
                c.create_oval(ex-38,eye_y-20, ex+38,eye_y+20,
                             fill="", outline=glow_col, width=1,
                             dash=(2,3), tags="dynamic")

                # Speaking particles
                if is_s and random.random() > 0.6:
                    px = ex + random.randint(-28, 28)
                    py = eye_y + random.randint(-15, 15)
                    r  = random.randint(1, 3)
                    c.create_oval(px-r,py-r,px+r,py+r, fill=CYAN, outline="", tags="dynamic")
            else:
                # Blink cover
                c.create_polygon([ex-28,eye_y-1, ex+28,eye_y-1, ex+24,eye_y+15, ex-24,eye_y+15],
                                fill="#030c16", outline="", tags="dynamic")

        # Nose bridge
        ns = [fcx-13,eye_y+20, fcx-16,fcy+12, fcx-9,fcy+26,
              fcx+9,fcy+26, fcx+16,fcy+12, fcx+13,eye_y+20]
        c.create_polygon(ns, fill="#112332", outline=CYAN2, width=1, tags="dynamic")

        # Upper faceplate
        uf = [fcx-60,fcy+26, fcx-66,fcy+38, fcx-44,fcy+57, fcx,fcy+63,
              fcx+44,fcy+57, fcx+66,fcy+38, fcx+60,fcy+26, fcx,fcy+20]
        c.create_polygon(uf, fill="#0f2035", outline=CYAN, width=1, tags="dynamic")

        # Upper vents
        for i in range(-2, 3):
            vx = fcx + i*23
            vy = fcy + 40
            c.create_rectangle(vx-9, vy-3, vx+9, vy+3,
                               fill="#001828", outline=CYAN, width=1, tags="dynamic")

        # Jaw (animated)
        j_off = jaw_o * 24
        jy    = fcy + 65 + j_off
        jaw   = [fcx-60,jy, fcx-66,jy+14, fcx-44,jy+33, fcx,jy+39,
                 fcx+44,jy+33, fcx+66,jy+14, fcx+60,jy, fcx,jy-6]
        c.create_polygon(jaw, fill="#0d1f2e", outline=CYAN, width=1, tags="dynamic")

        # Jaw vents
        for i in [-1, 0, 1]:
            vx = fcx + i*26
            vy = jy + 18
            c.create_rectangle(vx-10,vy-3, vx+10,vy+2,
                               fill="#001422", outline=CYAN2, width=1, tags="dynamic")

        # Jaw gap glow
        if jaw_o > 0.04:
            c.create_rectangle(fcx-56, fcy+63, fcx+56, jy+1,
                               fill="#001422", outline="", tags="dynamic")
            c.create_line(fcx-52,fcy+64, fcx+52,fcy+64, fill=CYAN, width=1, tags="dynamic")
            c.create_line(fcx-52,jy,     fcx+52,jy,     fill=CYAN, width=1, tags="dynamic")

        # Chin armor
        ch_y = jy + 39
        ch   = [fcx-54,ch_y, fcx-30,ch_y+54, fcx-18,ch_y+76, fcx,ch_y+80,
                fcx+18,ch_y+76, fcx+30,ch_y+54, fcx+54,ch_y,
                fcx+36,ch_y-10, fcx,ch_y-4, fcx-36,ch_y-10]
        c.create_polygon(ch, fill="#0a1720", outline=CYAN2, width=1, tags="dynamic")

        # HUD arcs
        ha  = 0.2 + 0.14 * math.sin(self._hud_phase)
        arc_col = self._rgba_color(CYAN, ha)
        # Top arc
        c.create_arc(fcx-172,fcy-172, fcx+172,fcy+172,
                    start=38, extent=116, style="arc",
                    outline=arc_col, width=1, tags="dynamic")
        # Bottom arc
        c.create_arc(fcx-172,fcy-172, fcx+172,fcy+172,
                    start=218, extent=116, style="arc",
                    outline=arc_col, width=1, tags="dynamic")

        # HUD text
        mode_txt = {
            "speaking":  "SPEAKING...",
            "listening": "LISTENING...",
            "alert":     "THREAT DETECTED",
            "idle":      "STANDBY",
        }.get(self.mode, "STANDBY")
        txt_col = RED if is_a else CYAN2
        c.create_text(16, 14, text="SYS:OK", fill=CYAN2, font=("Courier",7), anchor="w", tags="dynamic")
        c.create_text(16, 24, text="NET:ON", fill=CYAN2, font=("Courier",7), anchor="w", tags="dynamic")
        c.create_text(W-16, 14, text="ALERT!" if is_a else "SHIELD", fill=RED if is_a else CYAN2, font=("Courier",7), anchor="e", tags="dynamic")
        c.create_text(W-16, 24, text="SCAN", fill=CYAN2, font=("Courier",7), anchor="e", tags="dynamic")
        c.create_text(W//2, H-8, text=mode_txt, fill=txt_col, font=("Courier",7), anchor="s", tags="dynamic")

    # ─────────────────────────────────────────────────────────
    # DRAW ARC REACTOR
    # ─────────────────────────────────────────────────────────
    def _draw_arc(self):
        c   = self._arc_canvas
        c.delete("all")
        W,H = 150, 80
        cx,cy = W//2, H//2
        ap  = 0.6 + 0.4 * math.sin(self._arc_phase)

        # Rings
        for r, alpha in [(36,0.28),(28,0.19),(20,0.12)]:
            col = self._rgba_color(CYAN, alpha)
            c.create_oval(cx-r,cy-r,cx+r,cy+r, fill="", outline=col, width=1)

        # Hex petals
        for i in range(6):
            a  = i * math.pi / 3 + self._arc_phase * 0.35
            hx = cx + 17 * math.cos(a)
            hy = cy + 17 * math.sin(a)
            self._hex_shape(c, hx, hy, 5.5,
                           self._rgba_color(CYAN, 0.18*ap),
                           self._rgba_color(CYAN, 0.45*ap))

        # Core
        col_core = self._rgba_color(CYAN, 0.22*ap)
        c.create_oval(cx-9,cy-9,cx+9,cy+9, fill=col_core, outline="")
        col_core2 = self._rgba_color(CYAN, 0.7*ap)
        c.create_oval(cx-5,cy-5,cx+5,cy+5, fill=col_core2, outline="")
        c.create_oval(cx-2,cy-2,cx+2,cy+2, fill="#ffffff", outline="")

    # ─────────────────────────────────────────────────────────
    # DRAW TRAFFIC WAVEFORM
    # ─────────────────────────────────────────────────────────
    def _draw_traffic(self):
        c   = self._traffic_canvas
        c.delete("all")
        W,H = 880, 55
        c.create_rectangle(0,0,W,H, fill=PANEL, outline="")

        for offset, color in [(0, GREEN), (4, CYAN)]:
            pts = []
            for i, v in enumerate(self._traffic):
                x = i * (W / len(self._traffic))
                y = H/2 - (v + offset*3) * 0.36
                pts.extend([x, y])
            if len(pts) >= 4:
                c.create_line(pts, fill=color, width=1, smooth=True)

    # ─────────────────────────────────────────────────────────
    # HELPER FUNCTIONS
    # ─────────────────────────────────────────────────────────
    def _oval_path(self, c, cx, cy, rx, ry, **kw):
        c.create_oval(cx-rx,cy-ry,cx+rx,cy+ry, tags="dynamic", **kw)

    def _hex_shape(self, c, cx, cy, r, fill, outline, tags="dynamic"):
        pts = []
        for i in range(6):
            a = i * math.pi / 3
            pts.extend([cx + r*math.cos(a), cy + r*math.sin(a)])
        c.create_polygon(pts, fill=fill, outline=outline, width=1, tags=tags)

    def _rgba_color(self, hex_col, alpha):
        """Simulate alpha by blending with black"""
        hex_col = hex_col.lstrip("#")
        r = int(hex_col[0:2], 16)
        g = int(hex_col[2:4], 16)
        b = int(hex_col[4:6], 16)
        r = int(r * alpha)
        g = int(g * alpha)
        b = int(b * alpha)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _lerp_color(self, hex1, hex2, t):
        r1,g1,b1 = int(hex1[0:2],16),int(hex1[2:4],16),int(hex1[4:6],16)
        r2,g2,b2 = int(hex2[0:2],16),int(hex2[2:4],16),int(hex2[4:6],16)
        r = int(r1 + (r2-r1)*t)
        g = int(g1 + (g2-g1)*t)
        b = int(b1 + (b2-b1)*t)
        return f"{r:02x}{g:02x}{b:02x}"

    def _hex_alpha(self, hex_col, alpha):
        return self._rgba_color(hex_col, alpha)

    # ─────────────────────────────────────────────────────────
    # BUTTON ACTIONS
    # ─────────────────────────────────────────────────────────
    def _sim_ddos(self):
        fake = [
            ("103.21.244.52", "Mumbai",    "India",   87),
            ("45.33.32.156",  "Dallas",    "USA",     142),
            ("198.199.88.1",  "Frankfurt", "Germany", 203),
        ]
        f = random.choice(fake)
        self.add_ddos(f[0], f[1], f[2], f[3] + random.randint(0,50))

    def _scan_anim(self):
        """Simulate scan animation on devices"""
        self.set_devices([
            {"name": "Samsung",  "ip": "192.168.1.2", "status": "OK"},
            {"name": "iPhone",   "ip": "192.168.1.3", "status": "OK"},
            {"name": "Laptop",   "ip": "192.168.1.4", "status": "OK"},
            {"name": "Router",   "ip": "192.168.1.1", "status": "OK"},
            {"name": "Xiaomi",   "ip": "192.168.1.5", "status": "WARN"},
            {"name": "Unknown",  "ip": "192.168.1.8", "status": "RISK"},
            {"name": "Unknown",  "ip": "192.168.1.11","status": "RISK"},
        ])

    # ─────────────────────────────────────────────────────────
    def run(self):
        self.root.mainloop()


# ─────────────────────────────────────────────────────────────
# Start in background thread (for cyberjarvis.py integration)
# ─────────────────────────────────────────────────────────────
def start_dashboard():
    """
    cyberjarvis.py mein yeh call karo:

        from dashboard import start_dashboard
        dash = start_dashboard()

        # Jarvis bole toh:
        dash.set_mode('speaking')

        # User bole toh:
        dash.set_mode('listening')

        # DDoS detect ho toh:
        dash.add_ddos(ip, city, country, packets)

        # Scan ke baad devices set karo:
        dash.set_devices([
            {"name": "Samsung", "ip": "192.168.1.2", "status": "OK"},
        ])
    """
    dash = None

    def _run():
        nonlocal dash
        dash = JarvisDashboard()
        dash.run()

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    time.sleep(1.5)  # wait for window to open
    return dash


# ─────────────────────────────────────────────────────────────
# Run standalone
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("[JARVIS DASHBOARD] Starting...")
    app = JarvisDashboard()
    app.run()