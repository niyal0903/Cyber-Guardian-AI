#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════╗
# ║   JARVIS CYBER AI — Iron Man HUD Desktop App                ║
# ║   Exact same as shown in image — Python Tkinter             ║
# ║                                                              ║
# ║   INSTALL: pip install psutil pillow                        ║
# ║   RUN:     python jarvis_desktop_hud.py                     ║
# ╚══════════════════════════════════════════════════════════════╝

import tkinter as tk
from tkinter import ttk, font
import threading
import time
import math
import socket
import os
import sys
import psutil
import subprocess
import webbrowser
from datetime import datetime
import concurrent.futures
import random

# ── Colors (exact same as image) ───────────────────────────────
BG       = "#020d18"      # Dark navy background
PANEL    = "#0a1828"      # Panel background
BORDER   = "#0d2535"      # Border color
CYAN     = "#00d4ff"      # Main cyan
GREEN    = "#00ff88"      # Green OK
RED      = "#ff2244"      # Red danger
YELLOW   = "#ffaa00"      # Yellow warning
DIM      = "#335566"      # Dimmed text
WHITE    = "#aaddff"      # Light text
DARK_RED = "#330a10"      # Dark red bg
DARK_GRN = "#0a2218"      # Dark green bg

# ── Import cyberjarvis functions ───────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from cyberjarvis import (
        scan_wifi_devices, detect_brand, port_scan,
        start_sniffer, traffic_counter, arp_table, PORT_INFO
    )
    JARVIS_OK = True
    print("[✓] cyberjarvis.py connected!")
except Exception as e:
    JARVIS_OK = False
    print(f"[!] Demo mode: {e}")


# ══════════════════════════════════════════════════════════════
# MAIN HUD WINDOW
# ══════════════════════════════════════════════════════════════
class JarvisHUD:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JARVIS CYBER AI")
        self.root.configure(bg=BG)
        self.root.geometry("1200x900")
        self.root.resizable(True, True)

        # State
        self.devices    = []
        self.alerts     = []
        self.up_sec     = 0
        self.scanning   = False
        self.sniffing   = False
        self.ring_angle = 0
        self.scan_angle = 0
        self.traffic_data = [random.randint(15,60) for _ in range(60)]
        self.traffic_data2= [int(v*0.4) for v in self.traffic_data]
        self.bw_down    = 0.0
        self.bw_up      = 0.0
        self.bw_pkts    = 0
        self.net_prev   = None

        # Build UI
        self._build()
        self._start_timers()
        self.root.mainloop()

    # ── BUILD UI ───────────────────────────────────────────────
    def _build(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # TOP BAR
        self._topbar()

        # STAT CARDS
        self._stat_cards()

        # MAIN 3-COLUMN
        self._main_area()

        # TRAFFIC CHART
        self._traffic_panel()

        # BUTTONS
        self._buttons()

    def _topbar(self):
        f = tk.Frame(self.root, bg=BG)
        f.pack(fill="x", padx=14, pady=(14,0))

        # Separator line
        sep = tk.Frame(f, bg=BORDER, height=1)

        # Logo
        logo_f = tk.Frame(f, bg=BG)
        logo_f.pack(side="left")
        tk.Label(logo_f, text="JARVIS", font=("Courier New",20,"bold"),
                 fg=CYAN, bg=BG).pack(side="left")
        tk.Label(logo_f, text="  // CYBER AI v4.0",
                 font=("Courier New",10), fg=DIM, bg=BG).pack(side="left")

        # Right side
        right = tk.Frame(f, bg=BG)
        right.pack(side="right")

        self.dot_lbl = tk.Label(right, text="●", font=("Courier New",12),
                                fg=GREEN, bg=BG)
        self.dot_lbl.pack(side="left", padx=(0,4))
        tk.Label(right, text="ONLINE", font=("Courier New",10),
                 fg=GREEN, bg=BG).pack(side="left", padx=(0,12))
        self.clk_lbl = tk.Label(right, font=("Courier New",11),
                                fg=DIM, bg=BG)
        self.clk_lbl.pack(side="left")

        # Border line under topbar
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=14, pady=6)

    def _stat_cards(self):
        f = tk.Frame(self.root, bg=BG)
        f.pack(fill="x", padx=14, pady=(0,8))

        cards = [
            ("DEVICES",  "--",  CYAN,   "sv_dev"),
            ("UNKNOWN",  "--",  RED,    "sv_unk"),
            ("THREAT",   "--",  YELLOW, "sv_thr"),
            ("CPU",      "--",  GREEN,  "sv_cpu"),
            ("PACKETS",  "--",  WHITE,  "sv_pkt"),
        ]

        for i, (label, val, color, attr) in enumerate(cards):
            card = tk.Frame(f, bg=PANEL, bd=0, highlightthickness=1,
                           highlightbackground=BORDER)
            card.grid(row=0, column=i, padx=4, pady=2, sticky="nsew")
            f.grid_columnconfigure(i, weight=1)

            tk.Label(card, text=label, font=("Courier New",8),
                    fg=DIM, bg=PANEL).pack(pady=(10,2))
            lbl = tk.Label(card, text=val, font=("Courier New",22,"bold"),
                          fg=color, bg=PANEL)
            lbl.pack(pady=(0,10))
            setattr(self, attr, lbl)

    def _main_area(self):
        self.main_frame = tk.Frame(self.root, bg=BG)
        self.main_frame.pack(fill="both", expand=True, padx=14, pady=4)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # LEFT
        self._left_col()

        # CENTER HUD
        self._center_hud()

        # RIGHT
        self._right_col()

    def _panel(self, parent, title, row, col, padx=(4,4), pady=(0,8), sticky="nsew"):
        outer = tk.Frame(parent, bg=PANEL, highlightthickness=1,
                        highlightbackground=BORDER)
        outer.grid(row=row, column=col, padx=padx, pady=pady, sticky=sticky)
        tk.Label(outer, text=title, font=("Courier New",8),
                fg=DIM, bg=PANEL).pack(anchor="w", padx=10, pady=(8,2))
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x", padx=10)
        return outer

    def _left_col(self):
        col = tk.Frame(self.main_frame, bg=BG)
        col.grid(row=0, column=0, sticky="nsew", padx=(0,4))
        col.grid_rowconfigure(0, weight=2)
        col.grid_rowconfigure(1, weight=1)
        col.grid_rowconfigure(2, weight=1)

        # Network Devices panel
        dev_panel = tk.Frame(col, bg=PANEL, highlightthickness=1,
                            highlightbackground=BORDER)
        dev_panel.grid(row=0, column=0, sticky="nsew", pady=(0,6))
        tk.Label(dev_panel, text="NETWORK DEVICES", font=("Courier New",8),
                fg=DIM, bg=PANEL).pack(anchor="w", padx=10, pady=(8,2))
        tk.Frame(dev_panel, bg=BORDER, height=1).pack(fill="x", padx=10)
        self.dev_frame = tk.Frame(dev_panel, bg=PANEL)
        self.dev_frame.pack(fill="both", expand=True, padx=10, pady=6)
        tk.Label(self.dev_frame, text="Loading...", font=("Courier New",9),
                fg=DIM, bg=PANEL).pack(anchor="w")

        # Bandwidth panel
        bw_panel = tk.Frame(col, bg=PANEL, highlightthickness=1,
                           highlightbackground=BORDER)
        bw_panel.grid(row=1, column=0, sticky="nsew", pady=(0,6))
        tk.Label(bw_panel, text="BANDWIDTH", font=("Courier New",8),
                fg=DIM, bg=PANEL).pack(anchor="w", padx=10, pady=(8,2))
        tk.Frame(bw_panel, bg=BORDER, height=1).pack(fill="x", padx=10)
        self.bw_frame = tk.Frame(bw_panel, bg=PANEL)
        self.bw_frame.pack(fill="x", padx=10, pady=8)
        self._init_bw_bars()

        # Port scan panel
        port_panel = tk.Frame(col, bg=PANEL, highlightthickness=1,
                             highlightbackground=BORDER)
        port_panel.grid(row=2, column=0, sticky="nsew")
        tk.Label(port_panel, text="PORT SCAN", font=("Courier New",8),
                fg=DIM, bg=PANEL).pack(anchor="w", padx=10, pady=(8,2))
        tk.Frame(port_panel, bg=BORDER, height=1).pack(fill="x", padx=10)
        self.port_frame = tk.Frame(port_panel, bg=PANEL)
        self.port_frame.pack(fill="x", padx=10, pady=6)
        tk.Label(self.port_frame, text="Run scan to see ports...",
                font=("Courier New",9), fg=DIM, bg=PANEL).pack(anchor="w")

    def _init_bw_bars(self):
        bw_items = [
            ("Down", CYAN,   "bw_down_bar", "bw_down_lbl"),
            ("Up",   GREEN,  "bw_up_bar",   "bw_up_lbl"),
            ("Pkts", YELLOW, "bw_pkt_bar",  "bw_pkt_lbl"),
        ]
        for label, color, bar_attr, lbl_attr in bw_items:
            row = tk.Frame(self.bw_frame, bg=PANEL)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=("Courier New",9),
                    fg=DIM, bg=PANEL, width=5, anchor="w").pack(side="left")
            track = tk.Frame(row, bg="#0a1828", height=5)
            track.pack(side="left", fill="x", expand=True, padx=4)
            bar = tk.Frame(track, bg=color, height=5)
            bar.place(x=0, y=0, relwidth=0.3, height=5)
            setattr(self, bar_attr, bar)
            lbl = tk.Label(row, text="0 KB", font=("Courier New",9),
                          fg=CYAN, bg=PANEL, width=7, anchor="e")
            lbl.pack(side="right")
            setattr(self, lbl_attr, lbl)

    def _center_hud(self):
        self.canvas = tk.Canvas(self.main_frame, bg=BG, bd=0,
                               highlightthickness=0, width=380, height=480)
        self.canvas.grid(row=0, column=1, pady=4)
        self._draw_hud()

    def _draw_hud(self):
        c = self.canvas
        c.delete("all")
        cx, cy = 190, 240
        r_outer = 175

        # ── HUD RINGS ──────────────────────────────
        # Outermost faint ring
        c.create_oval(cx-r_outer, cy-r_outer, cx+r_outer, cy+r_outer,
                     outline=self._alpha_color(CYAN, 0.12), width=1)
        c.create_oval(cx-170, cy-170, cx+170, cy+170,
                     outline=self._alpha_color(CYAN, 0.2), width=1,
                     dash=(4,7))

        # Main rotating ring (drawn with offset angle)
        self._draw_arc_ring(c, cx, cy, 160, CYAN, 0.45, self.ring_angle, 1)

        # Scan arc (bright, counter-rotating)
        self._draw_scan_arc(c, cx, cy, 150, self.scan_angle)

        # Inner rings
        c.create_oval(cx-135, cy-135, cx+135, cy+135,
                     outline=self._alpha_color(CYAN, 0.18), width=1)
        self._draw_arc_ring(c, cx, cy, 128, CYAN, 0.28, -self.ring_angle*0.7, 1, (6,5))

        # Degree labels
        for angle, label in [(90,"0°"),(0,"90°"),(270,"180°"),(180,"270°")]:
            rad = math.radians(angle)
            lx  = cx + (r_outer+12) * math.cos(rad)
            ly  = cy - (r_outer+12) * math.sin(rad)
            c.create_text(lx, ly, text=label, fill=self._alpha_color(CYAN, 0.55),
                         font=("Courier New",7))

        # Corner brackets
        boff = 175
        for (x1,y1,x2,y2,x3,y3) in [
            (cx-boff,cy-boff, cx-boff,cy-boff+28, cx-boff+28,cy-boff),
            (cx+boff,cy-boff, cx+boff,cy-boff+28, cx+boff-28,cy-boff),
            (cx-boff,cy+boff, cx-boff,cy+boff-28, cx-boff+28,cy+boff),
            (cx+boff,cy+boff, cx+boff,cy+boff-28, cx+boff-28,cy+boff),
        ]:
            c.create_line(x1,y1,x2,y2, fill=self._alpha_color(CYAN,0.5), width=1.5)
            c.create_line(x1,y1,x3,y3, fill=self._alpha_color(CYAN,0.5), width=1.5)

        # Tick marks
        for angle in [0,45,90,135,180,225,270,315]:
            rad = math.radians(angle)
            x1 = cx + (r_outer-5)*math.cos(rad)
            y1 = cy - (r_outer-5)*math.sin(rad)
            x2 = cx + (r_outer+5)*math.cos(rad)
            y2 = cy - (r_outer+5)*math.sin(rad)
            c.create_line(x1,y1,x2,y2, fill=self._alpha_color(CYAN,0.3), width=0.8)

        # HUD header text
        c.create_text(cx, cy-r_outer-14, text="JARVIS CYBER AI // NETWORK SCAN",
                     fill=DIM, font=("Courier New",6))

        # Scan line
        sl_y = cy + int(math.sin(self.scan_angle*math.pi/180) * 120)
        c.create_line(cx-130, sl_y, cx+130, sl_y,
                     fill=self._alpha_color(CYAN, 0.08), width=0.5)

        # SYS / NET / MED / OK labels
        threat_col = RED if getattr(self,'_threat','Low')=='High' else YELLOW if getattr(self,'_threat','Low')=='Medium' else GREEN
        c.create_text(cx-115, cy-80, text="SYS", fill=self._alpha_color(CYAN,0.65), font=("Courier New",7))
        c.create_text(cx+115, cy-80, text="NET", fill=self._alpha_color(CYAN,0.65), font=("Courier New",7))
        c.create_text(cx-115, cy+80, text=getattr(self,'_threat','MED')[:3].upper(),
                     fill=threat_col, font=("Courier New",7))
        c.create_text(cx+115, cy+80, text="OK", fill=GREEN, font=("Courier New",7))

        # ── IRON MAN FACE ───────────────────────────
        self._draw_ironman_face(c, cx, cy)

    def _draw_ironman_face(self, c, cx, cy):
        """Draw exact Iron Man face from image."""

        # Outer red helmet shell
        pts = self._helmet_shell(cx, cy)
        c.create_polygon(pts, fill="#880000", outline="#550000", width=1, smooth=True)

        # Gold faceplate
        gpts = self._faceplate(cx, cy)
        c.create_polygon(gpts, fill="#8a6000", outline="#664400", width=1, smooth=True)
        c.create_polygon(gpts, fill="#b08000", outline="#885500", width=0.5, smooth=True)

        # Left cheek red
        lc = [cx-96,cy-42, cx-85,cy-52, cx-62,cy-48, cx-62,cy+14, cx-85,cy+18, cx-98,cy+8]
        c.create_polygon(lc, fill="#770000", outline="#440000", width=0.8)

        # Right cheek red
        rc = [cx+96,cy-42, cx+85,cy-52, cx+62,cy-48, cx+62,cy+14, cx+85,cy+18, cx+98,cy+8]
        c.create_polygon(rc, fill="#770000", outline="#440000", width=0.8)

        # Left forehead red
        lf = [cx-95,cy-90, cx-84,cy-102, cx-44,cy-104, cx-44,cy-78, cx-62,cy-72, cx-80,cy-78]
        c.create_polygon(lf, fill="#770000", outline="#440000", width=0.8)

        # Right forehead red
        rf = [cx+95,cy-90, cx+84,cy-102, cx+44,cy-104, cx+44,cy-78, cx+62,cy-72, cx+80,cy-78]
        c.create_polygon(rf, fill="#770000", outline="#440000", width=0.8)

        # Gold forehead center
        gf = [cx-44,cy-104, cx,cy-114, cx+44,cy-104, cx+44,cy-78, cx,cy-84, cx-44,cy-78]
        c.create_polygon(gf, fill="#aa8000", outline="#886600", width=0.8)
        c.create_line(cx,cy-113, cx,cy-84, fill="#ffe066", width=1)

        # Gold nose
        npts = [cx-12,cy+9, cx-8,cy-2, cx,cy-4, cx+8,cy-2, cx+12,cy+9, cx+8,cy+24, cx,cy+27, cx-8,cy+24]
        c.create_polygon(npts, fill="#aa8000", outline="#886600", width=0.8)

        # Gold chin + grille
        chin = [cx-30,cy+68, cx-36,cy+82, cx-32,cy+96, cx-16,cy+100, cx,cy+102,
                cx+16,cy+100, cx+32,cy+96, cx+36,cy+82, cx+30,cy+68,
                cx+18,cy+71, cx,cy+74, cx-18,cy+71]
        c.create_polygon(chin, fill="#996600", outline="#774400", width=0.8)
        for dx in [-18,-8,0,8,18]:
            c.create_line(cx+dx,cy+76, cx+dx,cy+92, fill="#664400", width=1)

        # Bottom side red
        c.create_polygon([cx-68,cy+88, cx-58,cy+90, cx-52,cy+103, cx-58,cy+114, cx-70,cy+111, cx-78,cy+100],
                        fill="#660000", outline="#440000", width=0.7)
        c.create_polygon([cx+68,cy+88, cx+58,cy+90, cx+52,cy+103, cx+58,cy+114, cx+70,cy+111, cx+78,cy+100],
                        fill="#660000", outline="#440000", width=0.7)

        # ── LEFT EYE ─────────────────────────────
        leye = [cx-82,cy-34, cx-72,cy-46, cx-42,cy-43, cx-34,cy-32, cx-38,cy-12, cx-52,cy-5, cx-76,cy-8, cx-85,cy-20]
        c.create_polygon(leye, fill="#040c14", outline="#001830", width=1)
        # Outer glow
        c.create_oval(cx-82,cy-46, cx-34,cy-5, outline=self._alpha_color(CYAN,0.1), width=10)
        # Main eye light
        c.create_polygon(leye, fill="#004466", outline="#00668a", width=0.5)
        # Bright center
        c.create_oval(cx-70,cy-36, cx-44,cy-16, fill="#00aacc", outline="#00d4ff", width=1)
        c.create_oval(cx-62,cy-31, cx-52,cy-21, fill="#88eeff", outline="white", width=0.5)
        c.create_oval(cx-59,cy-29, cx-55,cy-23, fill="white")
        # Eye highlight line
        c.create_line(cx-80,cy-33, cx-72,cy-44, cx-44,cy-41, cx-36,cy-30,
                     fill=self._alpha_color("white",0.3), width=1)

        # ── RIGHT EYE ────────────────────────────
        reye = [cx+82,cy-34, cx+72,cy-46, cx+42,cy-43, cx+34,cy-32, cx+38,cy-12, cx+52,cy-5, cx+76,cy-8, cx+85,cy-20]
        c.create_polygon(reye, fill="#040c14", outline="#001830", width=1)
        c.create_oval(cx+34,cy-46, cx+82,cy-5, outline=self._alpha_color(CYAN,0.1), width=10)
        c.create_polygon(reye, fill="#004466", outline="#00668a", width=0.5)
        c.create_oval(cx+44,cy-36, cx+70,cy-16, fill="#00aacc", outline="#00d4ff", width=1)
        c.create_oval(cx+52,cy-31, cx+62,cy-21, fill="#88eeff", outline="white", width=0.5)
        c.create_oval(cx+55,cy-29, cx+59,cy-23, fill="white")
        c.create_line(cx+80,cy-33, cx+72,cy-44, cx+44,cy-41, cx+36,cy-30,
                     fill=self._alpha_color("white",0.3), width=1)

        # Gold faceplate center lines
        c.create_line(cx,cy-84, cx,cy-44, fill="#ffe066", width=0.8)
        c.create_line(cx,cy+30, cx,cy+68, fill="#ffe066", width=0.7)

        # Red rim top highlight
        c.create_arc(cx-100,cy-120, cx+100,cy-60, start=0, extent=180,
                    style="arc", outline=self._alpha_color(RED,0.35), width=1)

        # Arc reactor (chest dot)
        c.create_oval(cx-12,cy+104, cx+12,cy+128, fill="#001525", outline=CYAN, width=1)
        c.create_oval(cx-8, cy+108, cx+8, cy+124, fill=CYAN, outline="white", width=0.5)
        c.create_oval(cx-3, cy+113, cx+3, cy+119, fill="white")

    def _helmet_shell(self, cx, cy):
        # Approximate Iron Man helmet outline as polygon points
        pts = []
        points_def = [
            (0,-142),(28,-138),(52,-126),(72,-108),(84,-84),
            (94,-58),(98,-30),(98,2),(92,32),(80,58),
            (68,80),(60,98),(58,112),(54,130),(48,144),
            (38,156),(20,164),(0,166),(-20,164),(-38,156),
            (-48,144),(-54,130),(-58,112),(-60,98),(-68,80),
            (-80,58),(-92,32),(-98,2),(-98,-30),(-94,-58),
            (-84,-84),(-72,-108),(-52,-126),(-28,-138),
        ]
        for dx,dy in points_def:
            pts.extend([cx+dx, cy+dy])
        return pts

    def _faceplate(self, cx, cy):
        pts = []
        fp = [
            (0,-112),(22,-110),(40,-100),(52,-84),(58,-62),
            (62,-38),(62,-10),(60,18),(56,42),(52,58),
            (46,72),(38,84),(28,92),(16,96),(0,98),
            (-16,96),(-28,92),(-38,84),(-46,72),(-52,58),
            (-56,42),(-60,18),(-62,-10),(-62,-38),(-58,-62),
            (-52,-84),(-40,-100),(-22,-110),
        ]
        for dx,dy in fp:
            pts.extend([cx+dx, cy+dy])
        return pts

    def _draw_arc_ring(self, c, cx, cy, r, color, alpha, offset, width, dash=None):
        steps = 72
        for i in range(steps):
            a1 = math.radians(offset + i*5)
            a2 = math.radians(offset + (i+1)*5)
            if i % 2 == 0:
                x1 = cx + r*math.cos(a1); y1 = cy - r*math.sin(a1)
                x2 = cx + r*math.cos(a2); y2 = cy - r*math.sin(a2)
                c.create_line(x1,y1,x2,y2, fill=self._alpha_color(color,alpha), width=width)

    def _draw_scan_arc(self, c, cx, cy, r, angle):
        arc_span = 55
        for i in range(arc_span):
            a = math.radians(angle - i)
            alpha = (arc_span - i) / arc_span * 0.9
            x1 = cx + (r-4)*math.cos(a); y1 = cy - (r-4)*math.sin(a)
            x2 = cx + (r+4)*math.cos(a); y2 = cy - (r+4)*math.sin(a)
            c.create_line(x1,y1,x2,y2, fill=self._alpha_color(CYAN,alpha), width=2)

    def _alpha_color(self, color, alpha):
        """Simulate alpha by blending with background."""
        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2],16) for i in (0,2,4))
        def rgb_to_hex(r,g,b):
            return f"#{r:02x}{g:02x}{b:02x}"
        try:
            fr,fg,fb = hex_to_rgb(color)
            br,bg_,bb = hex_to_rgb(BG)
            nr = int(br + (fr-br)*alpha)
            ng = int(bg_ + (fg-bg_)*alpha)
            nb = int(bb + (fb-bb)*alpha)
            return rgb_to_hex(max(0,min(255,nr)), max(0,min(255,ng)), max(0,min(255,nb)))
        except:
            return color

    def _right_col(self):
        col = tk.Frame(self.main_frame, bg=BG)
        col.grid(row=0, column=2, sticky="nsew", padx=(4,0))
        col.grid_rowconfigure(0, weight=2)
        col.grid_rowconfigure(1, weight=1)
        col.grid_rowconfigure(2, weight=1)

        # Live Alerts
        alerts_panel = tk.Frame(col, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
        alerts_panel.grid(row=0, column=0, sticky="nsew", pady=(0,6))
        tk.Label(alerts_panel, text="LIVE ALERTS", font=("Courier New",8),
                fg=DIM, bg=PANEL).pack(anchor="w", padx=10, pady=(8,2))
        tk.Frame(alerts_panel, bg=BORDER, height=1).pack(fill="x", padx=10)
        self.alert_frame = tk.Frame(alerts_panel, bg=PANEL)
        self.alert_frame.pack(fill="both", expand=True, padx=10, pady=6)

        # Port Scan
        port_panel = tk.Frame(col, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
        port_panel.grid(row=1, column=0, sticky="nsew", pady=(0,6))
        tk.Label(port_panel, text="PORT SCAN", font=("Courier New",8),
                fg=DIM, bg=PANEL).pack(anchor="w", padx=10, pady=(8,2))
        tk.Frame(port_panel, bg=BORDER, height=1).pack(fill="x", padx=10)
        self.port_right_frame = tk.Frame(port_panel, bg=PANEL)
        self.port_right_frame.pack(fill="x", padx=10, pady=6)
        self._default_ports()

        # System Health
        sys_panel = tk.Frame(col, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
        sys_panel.grid(row=2, column=0, sticky="nsew")
        tk.Label(sys_panel, text="SYSTEM", font=("Courier New",8),
                fg=DIM, bg=PANEL).pack(anchor="w", padx=10, pady=(8,2))
        tk.Frame(sys_panel, bg=BORDER, height=1).pack(fill="x", padx=10)
        sys_f = tk.Frame(sys_panel, bg=PANEL)
        sys_f.pack(fill="x", padx=10, pady=6)

        rows = [
            ("Uptime",   WHITE,  "sys_uptime"),
            ("RAM",      GREEN,  "sys_ram"),
            ("Firewall", GREEN,  None),
            ("IDS",      GREEN,  None),
            ("Sniffer",  YELLOW, "sys_sniff"),
        ]
        vals = ["00:00:00","--","ACTIVE","ONLINE","STANDBY"]
        for i, (label, color, attr) in enumerate(rows):
            r = tk.Frame(sys_f, bg=PANEL)
            r.pack(fill="x", pady=1)
            tk.Label(r, text=label, font=("Courier New",9), fg=DIM, bg=PANEL).pack(side="left")
            v = vals[i] if attr is None else vals[i]
            col_use = GREEN if label in ["Firewall","IDS"] else color
            lbl = tk.Label(r, text=v, font=("Courier New",9,"bold"), fg=col_use, bg=PANEL)
            lbl.pack(side="right")
            if attr:
                setattr(self, attr, lbl)

    def _default_ports(self):
        for w in self.port_right_frame.winfo_children():
            w.destroy()
        DANGER_PORTS = [21,23,135,139,445,1433,3306,3389,4444,5900]
        PORT_NAMES   = {21:"FTP",22:"SSH",23:"Telnet",80:"HTTP",443:"HTTPS",
                        445:"SMB",3306:"MySQL",3389:"RDP",8080:"HTTP-Alt",22:"SSH"}
        defaults = [(80,"HTTP",YELLOW),(443,"HTTPS",GREEN),(445,"SMB",RED),(22,"SSH",CYAN),(3389,"RDP",RED)]
        for port, name, color in defaults:
            r = tk.Frame(self.port_right_frame, bg=PANEL)
            r.pack(fill="x", pady=1)
            tk.Label(r, text=f"Port {port}", font=("Courier New",9), fg=DIM, bg=PANEL).pack(side="left")
            warn = " ⚠" if port in DANGER_PORTS else ""
            tk.Label(r, text=f"→ {name}{warn}", font=("Courier New",9,"bold"),
                    fg=color, bg=PANEL).pack(side="right")

    def _traffic_panel(self):
        panel = tk.Frame(self.root, bg=PANEL, highlightthickness=1, highlightbackground=BORDER)
        panel.pack(fill="x", padx=14, pady=(0,8))
        tk.Label(panel, text="LIVE NETWORK TRAFFIC", font=("Courier New",8),
                fg=DIM, bg=PANEL).pack(anchor="w", padx=10, pady=(8,2))
        tk.Frame(panel, bg=BORDER, height=1).pack(fill="x", padx=10)

        self.traffic_canvas = tk.Canvas(panel, bg=PANEL, height=90, bd=0, highlightthickness=0)
        self.traffic_canvas.pack(fill="x", padx=10, pady=8)
        self._draw_traffic()

    def _draw_traffic(self):
        c = self.traffic_canvas
        c.delete("all")
        w = c.winfo_width() or 1150
        h = 80

        def draw_wave(data, color, alpha=1.0):
            if len(data) < 2: return
            step = w / (len(data)-1)
            pts = []
            for i, v in enumerate(data):
                x = int(i * step)
                y = h - int(v / 120 * h)
                pts.extend([x, y])
            # Draw line
            for i in range(0, len(pts)-2, 2):
                col = self._alpha_color(color, alpha)
                c.create_line(pts[i],pts[i+1],pts[i+2],pts[i+3],
                             fill=col, width=1.5, smooth=True)

        draw_wave(self.traffic_data,  CYAN,  0.9)
        draw_wave(self.traffic_data2, GREEN, 0.7)

    def _buttons(self):
        f = tk.Frame(self.root, bg=BG)
        f.pack(fill="x", padx=14, pady=(0,14))

        buttons = [
            ("SCAN NETWORK",   self.do_scan,         CYAN),
            ("SIMULATE ALERT", self.sim_alert,        YELLOW),
            ("TRAFFIC SPIKE",  self.spike_traffic,    CYAN),
            ("BUILD DESKTOP APP ↗", self.build_info,  GREEN),
        ]

        for text, cmd, color in buttons:
            btn = tk.Button(
                f, text=text, command=cmd,
                font=("Courier New",10,"bold"),
                fg=color, bg=PANEL,
                activeforeground=color, activebackground=BORDER,
                relief="flat", bd=0, padx=20, pady=10,
                highlightthickness=1, highlightbackground=BORDER,
                cursor="hand2"
            )
            btn.pack(side="left", padx=4, fill="x", expand=True)

    # ── ACTIONS ────────────────────────────────────────────────
    def do_scan(self):
        if self.scanning: return
        self.scanning = True
        self.sv_dev.config(text="...")
        self.add_alert("Network scan started", CYAN)
        threading.Thread(target=self._scan_thread, daemon=True).start()

    def _scan_thread(self):
        try:
            if JARVIS_OK:
                devices = scan_wifi_devices()
            else:
                time.sleep(1.5)
                devices = [
                    ("192.168.1.1","aa:bb:cc:11:22:01","Router","JioFi"),
                    ("192.168.1.2","aa:bb:cc:11:22:02","Phone1","Apple Inc"),
                    ("192.168.1.3","aa:bb:cc:11:22:03","Phone2","Samsung Electronics"),
                    ("192.168.1.4","aa:bb:cc:11:22:04","Laptop","Intel Corporate"),
                    ("192.168.1.5","aa:bb:cc:11:22:05","TV","Samsung Electronics"),
                    ("192.168.1.8","ff:ee:dd:cc:bb:08","Unknown","Unknown Vendor"),
                    ("192.168.1.11","ff:ee:dd:cc:bb:11","Unknown","Unknown Vendor"),
                    ("192.168.1.6","aa:bb:cc:11:22:06","Home","Google LLC"),
                ]
            self.devices = devices
            self.root.after(0, lambda: self._update_devices(devices))
        except Exception as e:
            self.root.after(0, lambda: self.add_alert(f"Scan error: {e}", RED))
        self.scanning = False

    def _update_devices(self, devices):
        # Count
        unk = 0
        fmt_devs = []
        icons = {"apple":"A","samsung":"S","xiaomi":"X","oppo":"O","vivo":"V",
                "realme":"R","oneplus":"1","intel":"L","huawei":"H",
                "tp-link":"T","jio":"J","google":"G","hikvision":"C","microsoft":"M"}

        for ip, mac, name, vendor in devices:
            if JARVIS_OK:
                brand, dtype = detect_brand(vendor)
            else:
                v = vendor.lower()
                brand = "❓ Unknown"
                for k in icons:
                    if k in v: brand = f"✓ {k.title()}"; break
            is_unk = "Unknown" in brand or "❓" in brand
            if is_unk: unk += 1
            icon = "?"
            for k, l in icons.items():
                if k in vendor.lower(): icon = l; break
            fmt_devs.append((ip, mac, brand, icon, not is_unk))

        # Update stat cards
        self.sv_dev.config(text=str(len(devices)))
        self.sv_unk.config(text=str(unk))
        threat = "High" if unk>2 else "Medium" if unk>0 else "Low"
        self._threat = threat
        tcolor = RED if threat=="High" else YELLOW if threat=="Medium" else GREEN
        self.sv_thr.config(text=threat[:3].upper(), fg=tcolor)

        # Update device list
        for w in self.dev_frame.winfo_children():
            w.destroy()
        for ip, mac, brand, icon, trusted in fmt_devs[:7]:
            row = tk.Frame(self.dev_frame, bg=PANEL)
            row.pack(fill="x", pady=2)
            # Icon circle
            ico_bg = DARK_GRN if trusted else DARK_RED
            ico_fg = GREEN if trusted else RED
            ico = tk.Label(row, text=icon, font=("Courier New",9,"bold"),
                          fg=ico_fg, bg=ico_bg, width=2, relief="flat", bd=1)
            ico.pack(side="left", padx=(0,6))
            # Name+IP
            info = tk.Frame(row, bg=PANEL)
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=brand[:20], font=("Courier New",9),
                    fg=WHITE, bg=PANEL).pack(anchor="w")
            tk.Label(info, text=ip, font=("Courier New",8),
                    fg=DIM, bg=PANEL).pack(anchor="w")
            # Badge
            badge_bg = DARK_GRN if trusted else DARK_RED
            badge_fg = GREEN if trusted else RED
            tk.Label(row, text="ok" if trusted else "!",
                    font=("Courier New",8,"bold"), fg=badge_fg, bg=badge_bg,
                    padx=4).pack(side="right")

        self.add_alert(f"Scan complete: {len(devices)} devices", GREEN)
        if unk > 0:
            self.add_alert(f"WARNING: {unk} unknown devices!", RED)

        # Background port scan
        threading.Thread(target=self._port_scan_bg, args=(devices,), daemon=True).start()

    def _port_scan_bg(self, devices):
        all_ports = []
        for ip, mac, name, vendor in devices[:3]:
            try:
                if JARVIS_OK:
                    ports = port_scan(ip)
                else:
                    ports = [80, 443] if ip.endswith('.1') else []
                all_ports.extend(ports)
            except:
                pass
        if all_ports:
            self.root.after(0, lambda: self._update_ports(list(set(all_ports))))

    def _update_ports(self, ports):
        DANGER_PORTS = [21,23,135,139,445,1433,3306,3389,4444,5900]
        PORT_NAMES   = {21:"FTP",22:"SSH",23:"Telnet",80:"HTTP",443:"HTTPS",
                       445:"SMB",3306:"MySQL",3389:"RDP",8080:"HTTP-Alt"}
        for w in self.port_right_frame.winfo_children():
            w.destroy()
        for p in sorted(ports)[:6]:
            r = tk.Frame(self.port_right_frame, bg=PANEL)
            r.pack(fill="x", pady=1)
            tk.Label(r, text=f"Port {p}", font=("Courier New",9), fg=DIM, bg=PANEL).pack(side="left")
            name = PORT_NAMES.get(p, "Unknown")
            warn = " ⚠" if p in DANGER_PORTS else ""
            col = RED if p in DANGER_PORTS else GREEN if p in [22,443] else YELLOW
            tk.Label(r, text=f"→ {name}{warn}", font=("Courier New",9,"bold"),
                    fg=col, bg=PANEL).pack(side="right")

    def add_alert(self, msg, color=RED):
        now = datetime.now().strftime("%H:%M:%S")
        self.alerts.insert(0, (msg, color, now))
        if len(self.alerts) > 20:
            self.alerts.pop()
        self.root.after(0, self._render_alerts)

    def _render_alerts(self):
        for w in self.alert_frame.winfo_children():
            w.destroy()
        for msg, color, t in self.alerts[:7]:
            row = tk.Frame(self.alert_frame, bg=PANEL)
            row.pack(fill="x", pady=1)
            tk.Label(row, text="●", font=("Courier New",8),
                    fg=color, bg=PANEL).pack(side="left")
            tk.Label(row, text=msg[:38], font=("Courier New",8),
                    fg=DIM, bg=PANEL).pack(side="left", padx=4)
            tk.Label(row, text=t, font=("Courier New",7),
                    fg=DIM, bg=PANEL).pack(side="right")

    def sim_alert(self):
        msgs = [
            ("Port scan from 10.0.0.5", RED),
            ("New unknown device joined!", YELLOW),
            ("ARP spoof attempt blocked!", RED),
            ("DDoS flood: 850 pkt/s!", RED),
            ("Bandwidth spike detected", YELLOW),
        ]
        msg, color = random.choice(msgs)
        self.add_alert(msg, color)

    def spike_traffic(self):
        for i in range(10):
            self.traffic_data.pop(0)
            self.traffic_data.append(random.randint(80,115))
            self.traffic_data2.pop(0)
            self.traffic_data2.append(random.randint(45,65))
        self._draw_traffic()
        self.add_alert("Traffic spike: 850 pkt/s", RED)

    def build_info(self):
        self.add_alert("This IS the desktop app! Running locally.", GREEN)

    # ── TIMERS ─────────────────────────────────────────────────
    def _start_timers(self):
        self._tick_clock()
        self._tick_hud()
        self._tick_stats()
        self._tick_traffic()
        self._tick_uptime()

    def _tick_clock(self):
        self.clk_lbl.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self._tick_clock)

    def _tick_uptime(self):
        self.up_sec += 1
        h = str(self.up_sec//3600).zfill(2)
        m = str((self.up_sec%3600)//60).zfill(2)
        s = str(self.up_sec%60).zfill(2)
        if hasattr(self,'sys_uptime'):
            self.sys_uptime.config(text=f"{h}:{m}:{s}")
        # Blink dot
        cur = self.dot_lbl.cget("fg")
        self.dot_lbl.config(fg=BG if cur==GREEN else GREEN)
        self.root.after(1000, self._tick_uptime)

    def _tick_hud(self):
        self.ring_angle = (self.ring_angle + 1) % 360
        self.scan_angle = (self.scan_angle - 4) % 360
        self._draw_hud()
        self.root.after(50, self._tick_hud)

    def _tick_stats(self):
        cpu = psutil.cpu_percent(interval=0)
        ram = psutil.virtual_memory().percent

        self.sv_cpu.config(text=f"{int(cpu)}%")
        cpu_col = RED if cpu>80 else YELLOW if cpu>50 else GREEN
        self.sv_cpu.config(fg=cpu_col)
        if hasattr(self,'sys_ram'):
            self.sys_ram.config(text=f"{int(ram)}%")
            self.sys_ram.config(fg=RED if ram>80 else GREEN)

        # Network speed
        net = psutil.net_io_counters()
        if self.net_prev:
            pr, ps, pt = self.net_prev
            el = time.time() - pt
            if el > 0:
                rv = (net.bytes_recv - pr) / 1024 / el
                sv = (net.bytes_sent - ps) / 1024 / el
                pkts = int(rv/10 + sv/10)
                self.sv_pkt.config(text=str(pkts))

                def fmt(kb):
                    return f"{kb/1024:.1f}MB" if kb>1024 else f"{kb:.0f}KB"

                self.bw_down_lbl.config(text=fmt(rv))
                self.bw_up_lbl.config(text=fmt(sv))
                self.bw_pkt_lbl.config(text=f"{pkts}/s")

                # Update bar widths
                frame_w = self.bw_frame.winfo_width() or 260
                bar_w = max(10, frame_w - 80)
                for bar, val, mx in [
                    (self.bw_down_bar, rv,  500),
                    (self.bw_up_bar,   sv,  200),
                    (self.bw_pkt_bar,  pkts,300),
                ]:
                    rel = min(val/mx, 1.0) if mx>0 else 0
                    bar.place(x=0, y=0, relwidth=max(0.02,rel), height=5)

        self.net_prev = (net.bytes_recv, net.bytes_sent, time.time())
        self.root.after(2000, self._tick_stats)

    def _tick_traffic(self):
        net = psutil.net_io_counters()
        if self.net_prev:
            pr, ps, pt = self.net_prev
            el = max(time.time()-pt, 0.01)
            rv = (net.bytes_recv - pr) / 1024 / el
            sv = (net.bytes_sent - ps) / 1024 / el
            val  = min(int(rv/5), 115)
            val2 = min(int(sv/5), 60)
        else:
            val  = random.randint(15,60)
            val2 = int(val*0.4)
        self.traffic_data.pop(0); self.traffic_data.append(val)
        self.traffic_data2.pop(0); self.traffic_data2.append(val2)
        self._draw_traffic()
        self.root.after(800, self._tick_traffic)


# ══════════════════════════════════════════════════════════════
# INTEGRATION WITH CYBERJARVIS.PY
# ══════════════════════════════════════════════════════════════
"""
Apne cyberjarvis.py mein ye 3 cheezein add karo:

1. Top pe (imports mein):
   import subprocess

2. jarvis_loop se pehle:
   _hud_proc = None
   def launch_hud():
       global _hud_proc
       import time
       server = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_desktop_hud.py")
       if _hud_proc is None or _hud_proc.poll() is not None:
           _hud_proc = subprocess.Popen(["python", server])
           time.sleep(1)

3. jarvis_loop ke andar scan network se pehle:
   elif any(w in command for w in ["open hud","iron man","dashboard"]):
       speak("Opening Iron Man HUD sir")
       threading.Thread(target=launch_hud, daemon=True).start()
"""

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════╗
║   JARVIS IRON MAN HUD — DESKTOP APP         ║
║   Starting...                               ║
╚══════════════════════════════════════════════╝""")
    app = JarvisHUD()