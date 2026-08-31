"""
front_page.py — Professional Dashboard Launcher
================================================
Inventory Management System — Enhanced Front Page

HOW TO USE:
    Run this file:  python front_page.py
    Click "OPEN FULL APPLICATION" to launch the main app (plain.py)

NOTE: plain.py is NOT changed in any way.
"""

import tkinter as tk
from tkinter import ttk
import sqlite3
import subprocess
import sys
import os
from datetime import datetime
import windows   # ← all popup window functions

# ─────────────────────────────────────────────
#  DATABASE PATH (same folder as this script)
# ─────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH    = os.path.join(SCRIPT_DIR, "inventory.db")
PLAIN_PATH = os.path.join(SCRIPT_DIR, "plain.py")

# ─────────────────────────────────────────────
#  PREMIUM COLOR PALETTE
# ─────────────────────────────────────────────
BG_DARK        = "#0a0d14"
BG_CARD        = "#111520"
BG_CARD2       = "#161c2d"
BG_HOVER       = "#1f2740"
ACCENT_GREEN   = "#00d97e"
ACCENT_GREEN_H = "#00a85a"
ACCENT_BLUE    = "#3d8ef8"
ACCENT_YELLOW  = "#f59e0b"
ACCENT_RED     = "#ef4444"
ACCENT_PURPLE  = "#8957e5"
ACCENT_CYAN    = "#00d97e"
ACCENT_PINK    = "#f472b6"
ACCENT_SKY     = "#38bdf8"
TEXT_WHITE     = "#f0f4ff"
TEXT_LIGHT     = "#b8c1d8"
TEXT_GRAY      = "#6b7593"
BORDER         = "#232b45"
HEADER_BG      = "#0d1a1a"


# ══════════════════════════════════════════════════════════════════
#  MAIN APPLICATION CLASS
# ══════════════════════════════════════════════════════════════════
class InventoryDashboard:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Inventory Management System  —  Dashboard")
        self.root.geometry("1360x800")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)

        # Center window on screen
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = (sw // 2) - (1360 // 2)
        y  = (sh // 2) - (800  // 2)
        self.root.geometry(f"1360x800+{x}+{y}")

        # Connect to database
        self._connect_db()

        # Build the entire UI
        self._build_ui()

        # Start live clock
        self._tick_clock()

        # Start title pulse animation
        self._pulse_step = 0
        self._pulse_title()

        self.root.mainloop()

    # ──────────────────────────────────────────
    #  DATABASE
    # ──────────────────────────────────────────
    def _connect_db(self):
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.cur  = self.conn.cursor()
            self.db_ok = True
        except Exception:
            self.db_ok = False

    def _fetch_stats(self):
        """Read live counts from the database."""
        stats = {
            "stock"     : 0,
            "categories": 0,
            "parties"   : 0,
            "purchases" : 0,
            "sales"     : 0,
            "units"     : 0,
        }
        if not self.db_ok:
            return stats
        queries = {
            "stock"     : "SELECT COUNT(*) FROM stock",
            "categories": "SELECT COUNT(*) FROM category",
            "parties"   : "SELECT COUNT(*) FROM party",
            "purchases" : "SELECT COUNT(*) FROM Purchase",
            "sales"     : "SELECT COUNT(*) FROM sale",
            "units"     : "SELECT COUNT(*) FROM unit",
        }
        for key, sql in queries.items():
            try:
                self.cur.execute(sql)
                stats[key] = self.cur.fetchone()[0]
            except Exception:
                pass
        return stats

    # ──────────────────────────────────────────
    #  LAUNCH plain.py
    # ──────────────────────────────────────────
    def _launch_app(self, module=""):
        """Launch plain.py (the full inventory app) and close this dashboard."""
        try:
            # Show brief launching message
            if hasattr(self, '_status_lbl'):
                msg = f"Opening {module.strip()}..." if module else "Opening application..."
                self._status_lbl.config(text=f"  ●  {msg}", fg=ACCENT_GREEN)
                self.root.update()
            self.root.after(300, self._do_launch)
        except Exception as e:
            import tkinter.messagebox as mb
            mb.showerror("Error", f"Could not open plain.py:\n{e}")

    def _do_launch(self):
        try:
            subprocess.Popen([sys.executable, PLAIN_PATH], cwd=SCRIPT_DIR)
            self.root.destroy()
        except Exception as e:
            import tkinter.messagebox as mb
            mb.showerror("Error", f"Could not open plain.py:\n{e}")

    # ──────────────────────────────────────────
    #  REFRESH STATS (rebuild stat cards only)
    # ──────────────────────────────────────────
    def _refresh(self):
        stats = self._fetch_stats()
        for key, lbl in self._stat_labels.items():
            lbl.config(text=str(stats[key]))

    # ──────────────────────────────────────────
    #  LIVE CLOCK
    # ──────────────────────────────────────────
    def _tick_clock(self):
        now = datetime.now().strftime("%A, %d %B %Y   |   %I:%M:%S %p")
        self._clock_lbl.config(text=now)
        self.root.after(1000, self._tick_clock)

    # ──────────────────────────────────────────
    #  TITLE PULSE ANIMATION
    # ──────────────────────────────────────────
    def _pulse_title(self):
        shades = [TEXT_WHITE, "#d8e2ef", TEXT_LIGHT, "#d8e2ef", TEXT_WHITE]
        self._title_lbl.config(fg=shades[self._pulse_step % len(shades)])
        self._pulse_step += 1
        self.root.after(700, self._pulse_title)

    # ──────────────────────────────────────────
    #  HOVER HELPERS
    # ──────────────────────────────────────────
    @staticmethod
    def _bind_hover(widget, enter_bg, leave_bg,
                    enter_fg=TEXT_WHITE, leave_fg=TEXT_LIGHT):
        widget.bind("<Enter>", lambda e: widget.config(bg=enter_bg, fg=enter_fg))
        widget.bind("<Leave>", lambda e: widget.config(bg=leave_bg, fg=leave_fg))

    # ──────────────────────────────────────────
    #  BUILD ENTIRE UI
    # ──────────────────────────────────────────
    def _build_ui(self):
        stats = self._fetch_stats()
        self._stat_labels = {}   # key → Label widget (for refresh)

        # ════════ TOP HEADER BAR ════════
        header = tk.Frame(self.root, bg=BG_CARD2, height=64)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        # Left accent stripe
        tk.Frame(header, bg=ACCENT_GREEN, width=4).pack(side=tk.LEFT, fill=tk.Y)

        # Brand logo
        tk.Label(header,
                 text="📦  INVENTORY PRO",
                 font=("Helvetica", 16, "bold"),
                 bg=BG_CARD2, fg=TEXT_WHITE
                 ).pack(side=tk.LEFT, padx=(18, 0), pady=10)

        # Separator
        tk.Frame(header, bg=BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y, pady=10, padx=14)

        # Tagline
        tk.Label(header,
                 text="Smart Inventory. Real Results.",
                 font=("Helvetica", 9, "italic"),
                 bg=BG_CARD2, fg=TEXT_GRAY
                 ).pack(side=tk.LEFT)

        # Live indicator (right side)
        self._clock_lbl = tk.Label(header, text="",
                                    font=("Helvetica", 10),
                                    bg=BG_CARD2, fg=TEXT_LIGHT)
        self._clock_lbl.pack(side=tk.RIGHT, padx=20)

        tk.Label(header, text="●  LIVE",
                 font=("Helvetica", 9, "bold"),
                 bg=BG_CARD2, fg=ACCENT_GREEN
                 ).pack(side=tk.RIGHT, padx=5)

        # Bottom glow line
        tk.Frame(self.root, bg=ACCENT_GREEN, height=2).pack(fill=tk.X)
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill=tk.X)

        # ════════ MAIN BODY (sidebar + content) ════════
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True)

        # ── LEFT SIDEBAR ──
        self._build_sidebar(body)

        # ── RIGHT CONTENT ──
        content = tk.Frame(body, bg=BG_DARK)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_welcome(content)
        self._build_stat_cards(content, stats)
        self._build_divider(content, "MODULES — Click to open")
        self._build_module_buttons(content)
        self._build_action_buttons(content)

        # ════════ BOTTOM STATUS BAR ════════
        self._build_statusbar()

    # ──────────────────────────────────────────
    #  SIDEBAR
    # ──────────────────────────────────────────
    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=BG_CARD, width=240)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Top accent line in sidebar
        tk.Frame(sidebar, bg=ACCENT_GREEN, height=2).pack(fill=tk.X)

        # Section heading
        tk.Label(sidebar,
                 text="NAVIGATION",
                 font=("Helvetica", 8, "bold"),
                 bg=BG_CARD, fg=TEXT_GRAY
                 ).pack(anchor="w", padx=20, pady=(18, 6))

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill=tk.X, padx=12)

        # Sidebar nav items  →  each calls its specific window function
        nav_items = [
            ("📋   Management",    ACCENT_GREEN,  None),
            ("👥   Party Details", ACCENT_BLUE,   windows.open_party),
            ("🛒   Purchase",      ACCENT_YELLOW, windows.open_Purchase),
            ("💰   Sale",          ACCENT_RED,    windows.open_sale),
            ("📊   Reports",       ACCENT_PURPLE, windows.open_display),
            ("🏭   Godown",        ACCENT_GREEN,  windows.open_godown),
            ("🗄️   Database",     ACCENT_BLUE,   windows.open_database_viewer),
        ]

        for label, color, action in nav_items:
            row = tk.Frame(sidebar, bg=BG_CARD, cursor="hand2")
            row.pack(fill=tk.X, padx=8, pady=2)

            indicator = tk.Frame(row, bg=BG_CARD, width=3)
            indicator.pack(side=tk.LEFT, fill=tk.Y)

            lbl = tk.Label(row,
                           text=label,
                           font=("Helvetica", 10),
                           bg=BG_CARD, fg=TEXT_LIGHT,
                           anchor="w", padx=12, pady=9,
                           cursor="hand2")
            lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

            # Hover
            def on_enter(e, r=row, l=lbl, i=indicator, c=color):
                r.config(bg=BG_HOVER)
                l.config(bg=BG_HOVER, fg=c)
                i.config(bg=c)

            def on_leave(e, r=row, l=lbl, i=indicator):
                r.config(bg=BG_CARD)
                l.config(bg=BG_CARD, fg=TEXT_LIGHT)
                i.config(bg=BG_CARD)

            # Click → open the correct window
            def on_click(e, fn=action, name=label):
                if fn:
                    fn()         # open the popup window
                else:
                    self._launch_app(module=name)  # fallback

            row.bind("<Enter>", on_enter)
            row.bind("<Leave>", on_leave)
            row.bind("<Button-1>", on_click)
            lbl.bind("<Enter>", on_enter)
            lbl.bind("<Leave>", on_leave)
            lbl.bind("<Button-1>", on_click)
            indicator.bind("<Enter>", on_enter)
            indicator.bind("<Leave>", on_leave)
            indicator.bind("<Button-1>", on_click)

        # Spacer
        tk.Frame(sidebar, bg=BG_CARD).pack(fill=tk.BOTH, expand=True)

        # Bottom DB status badge
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill=tk.X, padx=12, pady=10)

        db_color = ACCENT_GREEN if self.db_ok else ACCENT_RED
        db_text  = "●  Database Connected" if self.db_ok else "●  Database Error"

        tk.Label(sidebar, text=db_text,
                 font=("Helvetica", 9, "bold"),
                 bg=BG_CARD, fg=db_color
                 ).pack(anchor="w", padx=20, pady=(0, 2))

        tk.Label(sidebar, text="  inventory.db",
                 font=("Helvetica", 8),
                 bg=BG_CARD, fg=TEXT_GRAY
                 ).pack(anchor="w", padx=20, pady=(0, 15))

    # ──────────────────────────────────────────
    #  WELCOME HEADING
    # ──────────────────────────────────────────
    def _build_welcome(self, parent):
        frame = tk.Frame(parent, bg=BG_DARK)
        frame.pack(fill=tk.X, padx=30, pady=(22, 5))

        self._title_lbl = tk.Label(
            frame,
            text="Inventory Management System",
            font=("Helvetica", 26, "bold"),
            bg=BG_DARK, fg=TEXT_WHITE, anchor="w"
        )
        self._title_lbl.pack(anchor="w")

        tk.Label(
            frame,
            text="Track your stock  •  Manage parties  •  Record purchases & sales  •  View reports",
            font=("Helvetica", 10),
            bg=BG_DARK, fg=TEXT_GRAY, anchor="w"
        ).pack(anchor="w", pady=(3, 0))

    # ──────────────────────────────────────────
    #  STAT CARDS
    # ──────────────────────────────────────────
    def _build_stat_cards(self, parent, stats):
        tk.Label(parent,
                 text="LIVE STATISTICS",
                 font=("Helvetica", 8, "bold"),
                 bg=BG_DARK, fg=TEXT_GRAY
                 ).pack(anchor="w", padx=30, pady=(12, 4))

        row = tk.Frame(parent, bg=BG_DARK)
        row.pack(fill=tk.X, padx=28)

        card_defs = [
            ("📦", "stock",      "Stock Items",  ACCENT_GREEN),
            ("🗂️",  "categories","Categories",   ACCENT_BLUE),
            ("👥", "parties",   "Parties",       ACCENT_YELLOW),
            ("🛒", "purchases", "Purchases",     ACCENT_RED),
            ("💰", "sales",     "Sales",         ACCENT_PURPLE),
            ("📏", "units",     "Units",         ACCENT_CYAN),
        ]

        for icon, key, label, color in card_defs:
            card = tk.Frame(row, bg=BG_CARD, relief="flat")
            card.pack(side=tk.LEFT, padx=4, pady=4, fill=tk.BOTH, expand=True)

            # Colored top accent bar
            tk.Frame(card, bg=color, height=3).pack(fill=tk.X)

            tk.Label(card, text=icon, font=("Helvetica", 18),
                     bg=BG_CARD, fg=color).pack(pady=(10, 0))

            val_lbl = tk.Label(card, text=str(stats[key]),
                               font=("Helvetica", 24, "bold"),
                               bg=BG_CARD, fg=TEXT_WHITE)
            val_lbl.pack()
            self._stat_labels[key] = val_lbl

            tk.Label(card, text=label, font=("Helvetica", 8, "bold"),
                     bg=BG_CARD, fg=TEXT_GRAY).pack(pady=(0, 10))

    # ──────────────────────────────────────────
    #  MODULE BUTTONS GRID
    # ──────────────────────────────────────────
    def _build_module_buttons(self, parent):
        outer = tk.Frame(parent, bg=BG_DARK)
        outer.pack(fill=tk.X, padx=28, pady=(4, 10))

        # Each module button mapped to its exact window function
        modules = [
            ("📏\nUnit\nMeasure",   ACCENT_GREEN,  windows.open_unit),
            ("📦\nStock\nItems",    ACCENT_BLUE,   windows.open_stock),
            ("🗂️\nCategory",        ACCENT_YELLOW, windows.open_category),
            ("🏭\nGodown",          ACCENT_PURPLE, windows.open_godown),
            ("👥\nParty\nDetails",  ACCENT_RED,    windows.open_party),
            ("🛒\nPurchase\nBill",  ACCENT_CYAN,   windows.open_Purchase),
            ("💰\nSale\nBill",      ACCENT_PINK,   windows.open_sale),
            ("📊\nDisplay\nStock",  ACCENT_SKY,    windows.open_display),
            ("🗄️\nDatabase\nViewer", "#00d97e",   windows.open_database_viewer),
        ]

        for text, color, action in modules:
            btn = tk.Label(
                outer,
                text=text,
                font=("Helvetica", 9, "bold"),
                bg=BG_CARD2, fg=TEXT_WHITE,
                width=10, height=5,
                relief="flat", cursor="hand2",
                justify="center"
            )
            btn.pack(side=tk.LEFT, padx=4, pady=4)

            self._bind_hover(btn,
                             enter_bg=color,  leave_bg=BG_CARD2,
                             enter_fg="white", leave_fg=TEXT_WHITE)

            btn.bind("<Button-1>", lambda e, fn=action: fn())

    # ──────────────────────────────────────────
    #  ACTION BUTTONS (Launch + Refresh)
    # ──────────────────────────────────────────
    def _build_action_buttons(self, parent):
        self._build_divider(parent, "ACTIONS")

        frame = tk.Frame(parent, bg=BG_DARK)
        frame.pack(anchor="w", padx=30, pady=6)

        # Primary — Launch App
        launch = tk.Button(
            frame,
            text="🚀   OPEN FULL APPLICATION",
            font=("Helvetica", 12, "bold"),
            bg=ACCENT_GREEN, fg="white",
            relief="flat", cursor="hand2",
            padx=28, pady=11,
            command=self._launch_app,
            activebackground=ACCENT_GREEN_H,
            activeforeground="white",
            bd=0
        )
        launch.pack(side=tk.LEFT, padx=(0, 8))

        launch.bind("<Enter>", lambda e: launch.config(bg=ACCENT_GREEN_H))
        launch.bind("<Leave>", lambda e: launch.config(bg=ACCENT_GREEN))

        # Secondary — Refresh stats
        refresh = tk.Button(
            frame,
            text="🔄   Refresh Stats",
            font=("Helvetica", 11),
            bg=BG_CARD, fg=TEXT_LIGHT,
            relief="flat", cursor="hand2",
            padx=20, pady=11,
            command=self._refresh,
            activebackground=BG_HOVER,
            activeforeground=TEXT_WHITE,
            bd=0
        )
        refresh.pack(side=tk.LEFT, padx=4)

        refresh.bind("<Enter>", lambda e: refresh.config(bg=BG_HOVER))
        refresh.bind("<Leave>", lambda e: refresh.config(bg=BG_CARD))

        # Info text
        tk.Label(
            frame,
            text="  ← Launches the main Inventory app  (plain.py)",
            font=("Helvetica", 9, "italic"),
            bg=BG_DARK, fg=TEXT_GRAY
        ).pack(side=tk.LEFT, padx=10)

    # ──────────────────────────────────────────
    #  SECTION DIVIDER
    # ──────────────────────────────────────────
    def _build_divider(self, parent, text=""):
        row = tk.Frame(parent, bg=BG_DARK)
        row.pack(fill=tk.X, padx=28, pady=(12, 4))

        tk.Frame(row, bg=BORDER, height=1).pack(side=tk.LEFT, fill=tk.Y,
                                                 expand=True, pady=8)
        if text:
            tk.Label(row, text=f"  {text}  ",
                     font=("Helvetica", 8, "bold"),
                     bg=BG_DARK, fg=TEXT_GRAY).pack(side=tk.LEFT)
            tk.Frame(row, bg=BORDER, height=1).pack(side=tk.LEFT, fill=tk.Y,
                                                     expand=True, pady=8)

    # ──────────────────────────────────────────
    #  STATUS BAR
    # ──────────────────────────────────────────
    def _build_statusbar(self):
        bar = tk.Frame(self.root, bg=BG_CARD2, height=28)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        bar.pack_propagate(False)

        tk.Frame(bar, bg=ACCENT_GREEN, width=4).pack(side=tk.LEFT, fill=tk.Y)

        self._status_lbl = tk.Label(
            bar,
            text="  ●  Ready   |   Inventory Management System  v2.0"
                 "   |   Python + SQLite3   |   Tkinter GUI",
            font=("Helvetica", 8),
            bg=BG_CARD2, fg=TEXT_GRAY
        )
        self._status_lbl.pack(side=tk.LEFT)

        tk.Label(bar,
                 text="Built with Python & Tkinter  ",
                 font=("Helvetica", 8),
                 bg=BG_CARD2, fg=TEXT_GRAY
                 ).pack(side=tk.RIGHT)


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════
if __name__ == "__main__":
    InventoryDashboard()
