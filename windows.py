"""
windows.py — Beautiful Popup Windows (Redesigned)
===================================================
All popup windows styled with a professional dark theme.
plain.py is NOT changed.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# ── Database ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH    = os.path.join(SCRIPT_DIR, "inventory.db")
conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()

# ── Premium Color Palette ──
BG_DARK      = "#0a0d14"
BG_CARD      = "#111520"
BG_CARD2     = "#161c2d"
BG_INPUT     = "#1a2035"
BG_HOVER     = "#1f2740"
ACCENT_GREEN = "#00d97e"
ACCENT_GRN_H = "#00a85a"
ACCENT_BLUE  = "#3d8ef8"
TEXT_WHITE   = "#f0f4ff"
TEXT_LIGHT   = "#b8c1d8"
TEXT_GRAY    = "#6b7593"
BORDER       = "#232b45"
BORDER_GLOW  = "#2e3d6b"
BTN_SAVE     = "#00d97e"
BTN_SEARCH   = "#3d8ef8"
BTN_DELETE   = "#ef4444"
BTN_UPDATE   = "#f59e0b"
BTN_CLEAR    = "#475569"


# ══════════════════════════════════════════════
#  SHARED HELPERS
# ══════════════════════════════════════════════

def _darken(hex_color, amount=30):
    r = max(0, int(hex_color[1:3], 16) - amount)
    g = max(0, int(hex_color[3:5], 16) - amount)
    b = max(0, int(hex_color[5:7], 16) - amount)
    return f"#{r:02x}{g:02x}{b:02x}"


def _lighten(hex_color, amount=20):
    r = min(255, int(hex_color[1:3], 16) + amount)
    g = min(255, int(hex_color[3:5], 16) + amount)
    b = min(255, int(hex_color[5:7], 16) + amount)
    return f"#{r:02x}{g:02x}{b:02x}"


def _center_window(win, width, height):
    win.update_idletasks()
    x = (win.winfo_screenwidth()  // 2) - (width  // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")


def _build_header(win, title, icon, subtitle="", accent=ACCENT_GREEN):
    """Premium header with badge icon, title, subtitle, and glow line."""
    hdr = tk.Frame(win, bg=BG_CARD2, height=78)
    hdr.pack(fill=tk.X)
    hdr.pack_propagate(False)
    # Left accent stripe
    tk.Frame(hdr, bg=accent, width=4).pack(side=tk.LEFT, fill=tk.Y)
    # Icon badge
    badge = tk.Frame(hdr, bg=accent, width=44, height=44)
    badge.pack(side=tk.LEFT, padx=(14, 0), pady=17)
    badge.pack_propagate(False)
    tk.Label(badge, text=icon, font=("Segoe UI Emoji", 16),
             bg=accent, fg="white").place(relx=0.5, rely=0.5, anchor="center")
    # Title + subtitle
    txt = tk.Frame(hdr, bg=BG_CARD2)
    txt.pack(side=tk.LEFT, padx=14)
    tk.Label(txt, text=title, font=("Helvetica", 15, "bold"),
             bg=BG_CARD2, fg=TEXT_WHITE, anchor="w").pack(anchor="w")
    if subtitle:
        tk.Label(txt, text=subtitle, font=("Helvetica", 8),
                 bg=BG_CARD2, fg=TEXT_GRAY, anchor="w").pack(anchor="w")
    # Bottom glow line
    tk.Frame(win, bg=accent, height=2).pack(fill=tk.X)
    tk.Frame(win, bg=BORDER, height=1).pack(fill=tk.X)


def _styled_entry(parent, var, row, col, width=30, colspan=1):
    e = tk.Entry(parent, textvariable=var, width=width,
                 bg=BG_INPUT, fg=TEXT_WHITE,
                 insertbackground=ACCENT_GREEN, relief="flat",
                 font=("Helvetica", 11),
                 highlightbackground=BORDER_GLOW,
                 highlightcolor=ACCENT_GREEN,
                 highlightthickness=1)
    e.grid(row=row, column=col, columnspan=colspan,
           sticky="ew", padx=(0, 20), pady=7)
    # Glow on focus
    e.bind("<FocusIn>",  lambda ev: e.config(highlightbackground=ACCENT_GREEN,
                                              highlightthickness=2))
    e.bind("<FocusOut>", lambda ev: e.config(highlightbackground=BORDER_GLOW,
                                              highlightthickness=1))
    return e


def _styled_combobox(parent, var, values, row, col, width=28, colspan=1):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Premium.TCombobox",
                    fieldbackground=BG_INPUT,
                    background=BG_INPUT,
                    foreground=TEXT_WHITE,
                    selectbackground=ACCENT_GREEN,
                    selectforeground="white",
                    bordercolor=BORDER_GLOW,
                    arrowcolor=TEXT_LIGHT,
                    padding=4)
    style.map("Premium.TCombobox",
              fieldbackground=[("readonly", BG_INPUT)],
              foreground=[("readonly", TEXT_WHITE)])
    cb = ttk.Combobox(parent, textvariable=var, values=values,
                      width=width, style="Premium.TCombobox",
                      font=("Helvetica", 11), state="readonly")
    cb.grid(row=row, column=col, columnspan=colspan,
            sticky="ew", padx=(0, 20), pady=7)
    return cb


def _label(parent, text, row, col, bold=False, size=10, color=TEXT_LIGHT):
    font = ("Helvetica", size, "bold") if bold else ("Helvetica", size)
    tk.Label(parent, text=text, font=font,
             bg=BG_CARD, fg=color, anchor="w"
             ).grid(row=row, column=col, sticky="w", padx=(20, 10), pady=7)


def _section_label(parent, text, row, colspan=4):
    tk.Frame(parent, bg=BORDER, height=1).grid(
        row=row, column=0, columnspan=colspan, sticky="ew", padx=15, pady=(10, 0))
    tk.Label(parent, text=f"  {text}  ",
             font=("Helvetica", 8, "bold"),
             bg=BG_CARD, fg=TEXT_GRAY
             ).grid(row=row, column=0, columnspan=colspan,
                    sticky="w", padx=20, pady=(10, 2))


def _btn_row(parent, row, colspan, save=None, search=None,
             delete=None, update=None, clear=None):
    """
    Premium 2-row button layout — buttons are NEVER cropped.
    Row 1: Save  Search  Delete
    Row 2: Update  Clear
    """
    outer = tk.Frame(parent, bg=BG_CARD)
    outer.grid(row=row, column=0, columnspan=colspan,
               sticky="ew", padx=15, pady=(8, 16))

    # Top divider
    tk.Frame(outer, bg=BORDER_GLOW, height=1).pack(fill=tk.X, pady=(0, 10))

    row1 = tk.Frame(outer, bg=BG_CARD)
    row1.pack(anchor="w")
    row2 = tk.Frame(outer, bg=BG_CARD)
    row2.pack(anchor="w", pady=(7, 0))

    def _make_btn(parent_frame, label, cmd, color):
        btn = tk.Button(
            parent_frame, text=label, command=cmd,
            bg=color, fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat", cursor="hand2",
            padx=20, pady=9, bd=0,
            activebackground=_darken(color),
            activeforeground="white"
        )
        btn.pack(side=tk.LEFT, padx=(0, 8))
        btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=_lighten(c, 15)))
        btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

    if save:   _make_btn(row1, "💾  Save",   save,   BTN_SAVE)
    if search: _make_btn(row1, "🔍  Search", search, BTN_SEARCH)
    if delete: _make_btn(row1, "🗑️  Delete", delete, BTN_DELETE)
    if update: _make_btn(row2, "✏️  Update", update, BTN_UPDATE)
    if clear:  _make_btn(row2, "✖  Clear",  clear,  BTN_CLEAR)


# ══════════════════════════════════════════════
#  UNIT OF MEASURE
# ══════════════════════════════════════════════
def open_unit():
    win = tk.Toplevel()
    win.title("Unit of Measure")
    win.configure(bg=BG_DARK)
    win.resizable(False, False)
    _center_window(win, 490, 410)
    _build_header(win, "Unit of Measure", "📏",
                  subtitle="Add / Edit measuring units  •  KG, Liter, Piece…")

    form = tk.Frame(win, bg=BG_CARD)
    form.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    form.columnconfigure(1, weight=1)

    Formal_Namevar = tk.StringVar()
    Full_Namevar   = tk.StringVar()

    _label(form, "Formal Name",  1, 0)
    _label(form, "Full Name",    2, 0)
    _styled_entry(form, Formal_Namevar, 1, 1)
    _styled_entry(form, Full_Namevar,   2, 1)
    form.rowconfigure(3, minsize=10)
    form.rowconfigure(4, minsize=10)

    def savedata():
        cur.execute("INSERT INTO unit VALUES(?,?)",
                    (Formal_Namevar.get().upper(), Full_Namevar.get().upper()))
        conn.commit()
        messagebox.showinfo("Saved ✅", "Unit saved successfully!")
        cleardata()

    def searchdata():
        cur.execute("SELECT * FROM unit WHERE Formal_Name=?",
                    (Formal_Namevar.get().upper(),))
        row = cur.fetchone()
        if row: Full_Namevar.set(row[1])
        else:
            messagebox.showinfo("Not Found", "No record found.")
            cleardata()

    def deletedata():
        cur.execute("DELETE FROM unit WHERE Formal_Name=?",
                    (Formal_Namevar.get().upper(),))
        conn.commit()
        messagebox.showinfo("Deleted 🗑️", "Record deleted.")
        cleardata()

    def updatedata():
        cur.execute("UPDATE unit SET Full_Name=? WHERE Formal_Name=?",
                    (Full_Namevar.get().upper(), Formal_Namevar.get().upper()))
        conn.commit()
        messagebox.showinfo("Updated ✏️", "Record updated.")
        cleardata()

    def cleardata():
        Formal_Namevar.set(""); Full_Namevar.set("")

    _btn_row(form, 5, 2,
             save=savedata, search=searchdata,
             delete=deletedata, update=updatedata, clear=cleardata)


# ══════════════════════════════════════════════
#  STOCK ITEMS
# ══════════════════════════════════════════════
def open_stock():
    win = tk.Toplevel()
    win.title("Stock Items")
    win.configure(bg=BG_DARK)
    win.resizable(False, False)
    _center_window(win, 530, 560)
    _build_header(win, "Stock Items", "📦",
                  subtitle="Manage inventory items, prices and GST rates")

    form = tk.Frame(win, bg=BG_CARD)
    form.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    form.columnconfigure(1, weight=1)

    cur.execute("SELECT category_Name FROM category")
    cat_list = [r[0] for r in cur.fetchall()]
    cur.execute("SELECT Formal_Name FROM unit")
    unit_list = [r[0] for r in cur.fetchall()]

    Item_Namevar    = tk.StringVar()
    Unit_Namevar    = tk.StringVar()
    Categoryvar     = tk.StringVar()
    Opening_itemvar = tk.StringVar()
    Pricevar        = tk.StringVar()
    GST_Ratevar     = tk.StringVar()

    _label(form, "Item Name",     1, 0)
    _label(form, "Unit Name",     2, 0)
    _label(form, "Category",      3, 0)
    _label(form, "Opening Stock", 4, 0)
    _label(form, "Price (₹)",     5, 0)
    _label(form, "GST Rate (%)",  6, 0)

    _styled_entry(form, Item_Namevar,    1, 1)
    _styled_combobox(form, Unit_Namevar, unit_list, 2, 1)
    _styled_combobox(form, Categoryvar,  cat_list,  3, 1)
    _styled_entry(form, Opening_itemvar, 4, 1)
    _styled_entry(form, Pricevar,        5, 1)
    _styled_entry(form, GST_Ratevar,     6, 1)
    form.rowconfigure(7, minsize=10)

    def savedata():
        try:
            cur.execute("INSERT INTO stock VALUES(?,?,?,?,?,?)",
                        (Item_Namevar.get().upper(), Unit_Namevar.get().upper(),
                         Categoryvar.get().upper(), Opening_itemvar.get(),
                         Pricevar.get(), GST_Ratevar.get()))
            conn.commit()
            messagebox.showinfo("Saved ✅", "Stock item saved!")
            cleardata()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def searchdata():
        cur.execute("SELECT * FROM stock WHERE Item_Name=?",
                    (Item_Namevar.get().upper(),))
        row = cur.fetchone()
        if row:
            Unit_Namevar.set(row[1]); Categoryvar.set(row[2])
            Opening_itemvar.set(row[3]); Pricevar.set(row[4])
            GST_Ratevar.set(row[5])
        else:
            messagebox.showinfo("Not Found", "No record found.")

    def deletedata():
        cur.execute("DELETE FROM stock WHERE Item_Name=?",
                    (Item_Namevar.get().upper(),))
        conn.commit()
        messagebox.showinfo("Deleted 🗑️", "Record deleted.")
        cleardata()

    def updatedata():
        cur.execute("UPDATE stock SET Unit_Name=?,category=?,Opening_item=?,price=?,GST_Rate=? WHERE Item_Name=?",
                    (Unit_Namevar.get().upper(), Categoryvar.get().upper(),
                     Opening_itemvar.get(), Pricevar.get(), GST_Ratevar.get(),
                     Item_Namevar.get().upper()))
        conn.commit()
        messagebox.showinfo("Updated ✏️", "Record updated.")
        cleardata()

    def cleardata():
        for v in [Item_Namevar, Unit_Namevar, Categoryvar,
                  Opening_itemvar, Pricevar, GST_Ratevar]:
            v.set("")

    _btn_row(form, 8, 2,
             save=savedata, search=searchdata,
             delete=deletedata, update=updatedata, clear=cleardata)


# ══════════════════════════════════════════════
#  CATEGORY
# ══════════════════════════════════════════════
def open_category():
    win = tk.Toplevel()
    win.title("Category")
    win.configure(bg=BG_DARK)
    win.resizable(False, False)
    _center_window(win, 490, 400)
    _build_header(win, "Category", "🗂️",
                  subtitle="Group items  •  Food, Electronics, Clothing…",
                  accent=ACCENT_BLUE)

    form = tk.Frame(win, bg=BG_CARD)
    form.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    form.columnconfigure(1, weight=1)

    category_Namevar     = tk.StringVar()
    category_fullNamevar = tk.StringVar()

    _label(form, "Category Name",      1, 0)
    _label(form, "Category Full Name", 2, 0)
    _styled_entry(form, category_Namevar,     1, 1)
    _styled_entry(form, category_fullNamevar, 2, 1)
    form.rowconfigure(3, minsize=10)
    form.rowconfigure(4, minsize=10)

    def savedata():
        try:
            cur.execute("INSERT INTO category VALUES(?,?)",
                        (category_Namevar.get().upper(), category_fullNamevar.get().upper()))
            conn.commit()
            messagebox.showinfo("Saved ✅", "Category saved!")
            cleardata()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def searchdata():
        cur.execute("SELECT * FROM category WHERE category_Name=?",
                    (category_Namevar.get().upper(),))
        row = cur.fetchone()
        if row: category_fullNamevar.set(row[1])
        else:
            messagebox.showinfo("Not Found", "No record found.")

    def deletedata():
        cur.execute("DELETE FROM category WHERE category_Name=?",
                    (category_Namevar.get().upper(),))
        conn.commit()
        messagebox.showinfo("Deleted 🗑️", "Deleted.")
        cleardata()

    def updatedata():
        cur.execute("UPDATE category SET category_fullName=? WHERE category_Name=?",
                    (category_fullNamevar.get().upper(), category_Namevar.get().upper()))
        conn.commit()
        messagebox.showinfo("Updated ✏️", "Updated.")
        cleardata()

    def cleardata():
        category_Namevar.set(""); category_fullNamevar.set("")

    _btn_row(form, 5, 2,
             save=savedata, search=searchdata,
             delete=deletedata, update=updatedata, clear=cleardata)


# ══════════════════════════════════════════════
#  GODOWN
# ══════════════════════════════════════════════
def open_godown():
    win = tk.Toplevel()
    win.title("Godown")
    win.configure(bg=BG_DARK)
    win.resizable(False, False)
    _center_window(win, 490, 430)
    _build_header(win, "Godown / Warehouse", "🏭",
                  subtitle="Manage storage locations and warehouse details",
                  accent="#8957e5")

    form = tk.Frame(win, bg=BG_CARD)
    form.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    form.columnconfigure(1, weight=1)

    godown_Namevar = tk.StringVar()
    godown_typevar = tk.StringVar()
    Addressvar     = tk.StringVar()

    _label(form, "Godown Name", 1, 0)
    _label(form, "Godown Type", 2, 0)
    _label(form, "Address",     3, 0)
    _styled_entry(form, godown_Namevar, 1, 1)
    _styled_entry(form, godown_typevar, 2, 1)
    _styled_entry(form, Addressvar,     3, 1)
    form.rowconfigure(4, minsize=10)

    def savedata():
        cur.execute("INSERT INTO godown VALUES(?,?,?)",
                    (godown_Namevar.get().upper(), godown_typevar.get().upper(),
                     Addressvar.get().upper()))
        conn.commit()
        messagebox.showinfo("Saved ✅", "Godown saved!")
        cleardata()

    def searchdata():
        cur.execute("SELECT * FROM godown WHERE godown_Name=?",
                    (godown_Namevar.get().upper(),))
        row = cur.fetchone()
        if row:
            godown_typevar.set(row[1]); Addressvar.set(row[2])
        else:
            messagebox.showinfo("Not Found", "No record found.")

    def deletedata():
        cur.execute("DELETE FROM godown WHERE godown_Name=?",
                    (godown_Namevar.get().upper(),))
        conn.commit()
        messagebox.showinfo("Deleted 🗑️", "Deleted.")
        cleardata()

    def updatedata():
        cur.execute("UPDATE godown SET godown_type=?,Address=? WHERE godown_Name=?",
                    (godown_typevar.get().upper(), Addressvar.get().upper(),
                     godown_Namevar.get().upper()))
        conn.commit()
        messagebox.showinfo("Updated ✏️", "Updated.")
        cleardata()

    def cleardata():
        godown_Namevar.set(""); godown_typevar.set(""); Addressvar.set("")

    _btn_row(form, 5, 2,
             save=savedata, search=searchdata,
             delete=deletedata, update=updatedata, clear=cleardata)


# ══════════════════════════════════════════════
#  PARTY DETAILS
# ══════════════════════════════════════════════
def open_party():
    win = tk.Toplevel()
    win.title("Party Details")
    win.configure(bg=BG_DARK)
    win.resizable(False, False)
    _center_window(win, 530, 570)
    _build_header(win, "Party Details", "👥",
                  subtitle="Manage customers (Debtors) and suppliers (Creditors)",
                  accent="#ef4444")

    form = tk.Frame(win, bg=BG_CARD)
    form.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    form.columnconfigure(1, weight=1)

    Company_Namevar = tk.StringVar()
    Party_typevar   = tk.StringVar()
    Addressvar      = tk.StringVar()
    Statevar        = tk.StringVar()
    Emailvar        = tk.StringVar()
    Mobilevar       = tk.StringVar()

    _label(form, "Company Name", 1, 0)
    _label(form, "Party Type",   2, 0)
    _label(form, "Address",      3, 0)
    _label(form, "State",        4, 0)
    _label(form, "Email",        5, 0)
    _label(form, "Mobile",       6, 0)

    _styled_entry(form, Company_Namevar, 1, 1)
    _styled_combobox(form, Party_typevar,
                     ["Sundry Creditor", "Sundry Debtor"], 2, 1)
    _styled_entry(form, Addressvar, 3, 1)
    _styled_entry(form, Statevar,   4, 1)
    _styled_entry(form, Emailvar,   5, 1)
    _styled_entry(form, Mobilevar,  6, 1)
    form.rowconfigure(7, minsize=10)

    def savedata():
        cur.execute("INSERT INTO party VALUES(?,?,?,?,?,?)",
                    (Company_Namevar.get().upper(), Party_typevar.get().upper(),
                     Addressvar.get().upper(), Statevar.get().upper(),
                     Emailvar.get().upper(), Mobilevar.get()))
        conn.commit()
        messagebox.showinfo("Saved ✅", "Party saved!")
        cleardata()

    def searchdata():
        cur.execute("SELECT * FROM party WHERE Company_Name=?",
                    (Company_Namevar.get().upper(),))
        row = cur.fetchone()
        if row:
            Party_typevar.set(row[1]); Addressvar.set(row[2])
            Statevar.set(row[3]); Emailvar.set(row[4]); Mobilevar.set(row[5])
        else:
            messagebox.showinfo("Not Found", "No record found.")

    def deletedata():
        cur.execute("DELETE FROM party WHERE Company_Name=?",
                    (Company_Namevar.get().upper(),))
        conn.commit()
        messagebox.showinfo("Deleted 🗑️", "Deleted.")
        cleardata()

    def updatedata():
        cur.execute("UPDATE party SET Party_type=?,Address=?,State=?,Email=?,Mobile=? WHERE Company_Name=?",
                    (Party_typevar.get().upper(), Addressvar.get().upper(),
                     Statevar.get().upper(), Emailvar.get().upper(),
                     Mobilevar.get(), Company_Namevar.get().upper()))
        conn.commit()
        messagebox.showinfo("Updated ✏️", "Updated.")
        cleardata()

    def cleardata():
        for v in [Company_Namevar, Party_typevar, Addressvar,
                  Statevar, Emailvar, Mobilevar]:
            v.set("")

    _btn_row(form, 8, 2,
             save=savedata, search=searchdata,
             delete=deletedata, update=updatedata, clear=cleardata)


# ══════════════════════════════════════════════
#  PURCHASE
# ══════════════════════════════════════════════
def open_Purchase():
    win = tk.Toplevel()
    win.title("Purchase Bill")
    win.configure(bg=BG_DARK)
    win.state("zoomed")   # full screen
    _build_header(win, "Purchase Bill", "🛒",
                  subtitle="Record purchases from suppliers  •  Stock auto-updates on save",
                  accent=ACCENT_GREEN)

    cur.execute("SELECT Company_Name FROM party WHERE Party_type=?", ("SUNDRY CREDITOR",))
    party_list = [r[0] for r in cur.fetchall()]
    cur.execute("SELECT Item_Name FROM stock")
    stock_list = [r[0] for r in cur.fetchall()]

    # ── Helper functions ──
    def get_party_details(pname):
        cur.execute("SELECT Address,Email,Mobile FROM party WHERE Company_Name=?", (pname,))
        r = cur.fetchall()
        return r[0] if r else ("", "", "")

    def get_price(iname):
        cur.execute("SELECT Price FROM stock WHERE Item_Name=?", (iname,))
        r = cur.fetchone()
        return float(r[0]) if r else 0.0

    def update_stock_qty(item, qty):
        if item:
            cur.execute("SELECT Opening_item FROM stock WHERE Item_Name=?", (item,))
            r = cur.fetchone()
            if r:
                cur.execute("UPDATE stock SET Opening_item=? WHERE Item_Name=?",
                            (float(r[0]) + float(qty), item))
                conn.commit()

    # ── Variables ──
    Billnovar = tk.StringVar(); DOBvar = tk.StringVar()
    CompanyVar = tk.StringVar(); AddrVar = tk.StringVar()
    EmailVar = tk.StringVar(); MobVar = tk.StringVar()
    item_vars = [tk.StringVar() for _ in range(5)]
    price_vars = [tk.StringVar() for _ in range(5)]
    qty_vars = [tk.StringVar() for _ in range(5)]
    amt_vars = [tk.StringVar() for _ in range(5)]
    TotalVar = tk.StringVar(); CostVar = tk.StringVar(); NetVar = tk.StringVar()
    CostVar.set("18")

    def calculate(index):
        try:
            p = float(price_vars[index].get() or 0)
            q = int(qty_vars[index].get() or 0)
            amt_vars[index].set(str(p * q))
            total = sum(float(a.get() or 0) for a in amt_vars)
            TotalVar.set(str(total))
            cost = float(CostVar.get() or 0)
            NetVar.set(str(round(total + total * cost / 100, 2)))
        except Exception as e:
            messagebox.showinfo("Calc Error", str(e))

    # ── Main scrollable container ──
    canvas = tk.Canvas(win, bg=BG_DARK, highlightthickness=0)
    scroll = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(fill=tk.BOTH, expand=True)

    container = tk.Frame(canvas, bg=BG_DARK)
    canvas.create_window((0, 0), window=container, anchor="nw")
    container.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))

    # ── SECTION: Bill Header ──
    sec1 = tk.Frame(container, bg=BG_CARD)
    sec1.pack(fill=tk.X, padx=20, pady=(15, 5))
    sec1.columnconfigure(1, weight=1); sec1.columnconfigure(3, weight=1)

    tk.Label(sec1, text="BILL DETAILS", font=("Helvetica", 9, "bold"),
             bg=BG_CARD, fg=TEXT_GRAY).grid(row=0, column=0, columnspan=4,
             sticky="w", padx=20, pady=(10, 2))
    tk.Frame(sec1, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4,
             sticky="ew", padx=15, pady=(0, 8))

    _label(sec1, "Bill No",          2, 0); _styled_entry(sec1, Billnovar, 2, 1)
    _label(sec1, "Date of Purchase", 2, 2); _styled_entry(sec1, DOBvar,    2, 3)

    _label(sec1, "Company Name", 3, 0)
    party_cb = _styled_combobox(sec1, CompanyVar, party_list, 3, 1)
    def on_party(e=None):
        a, m, mob = get_party_details(CompanyVar.get())
        AddrVar.set(a); EmailVar.set(m); MobVar.set(mob)
    party_cb.bind("<<ComboboxSelected>>", on_party)

    _label(sec1, "Address",   4, 0); _styled_entry(sec1, AddrVar,  4, 1)
    _label(sec1, "Email",     5, 0); _styled_entry(sec1, EmailVar, 5, 1)
    _label(sec1, "Mobile No", 5, 2); _styled_entry(sec1, MobVar,   5, 3)

    # ── SECTION: Items ──
    sec2 = tk.Frame(container, bg=BG_CARD)
    sec2.pack(fill=tk.X, padx=20, pady=5)

    tk.Label(sec2, text="ITEM DETAILS", font=("Helvetica", 9, "bold"),
             bg=BG_CARD, fg=TEXT_GRAY).grid(row=0, column=0, columnspan=4,
             sticky="w", padx=20, pady=(10, 2))
    tk.Frame(sec2, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4,
             sticky="ew", padx=15, pady=(0, 5))

    # Column headers
    for col, txt in enumerate(["Item Name", "Price (₹)", "Quantity", "Amount (₹)"]):
        tk.Label(sec2, text=txt, font=("Helvetica", 10, "bold"),
                 bg=BG_CARD, fg=ACCENT_GREEN
                 ).grid(row=2, column=col, padx=(20 if col==0 else 5, 5), pady=5, sticky="w")

    for i in range(5):
        row_num = 3 + i
        cb = _styled_combobox(sec2, item_vars[i], stock_list, row_num, 0, width=22)
        _styled_entry(sec2, price_vars[i], row_num, 1, width=12)
        qty_cb = _styled_combobox(sec2, qty_vars[i],
                                  [str(n) for n in range(1, 101)], row_num, 2, width=10)
        _styled_entry(sec2, amt_vars[i], row_num, 3, width=12)

        def make_handlers(idx):
            def on_item(e=None):
                price_vars[idx].set(str(get_price(item_vars[idx].get())))
                calculate(idx)
            def on_qty(e=None):
                calculate(idx)
            return on_item, on_qty

        on_item, on_qty = make_handlers(i)
        cb.bind("<<ComboboxSelected>>", on_item)
        qty_cb.bind("<<ComboboxSelected>>", on_qty)

    # ── SECTION: Totals ──
    sec3 = tk.Frame(container, bg=BG_CARD)
    sec3.pack(fill=tk.X, padx=20, pady=5)
    sec3.columnconfigure(1, weight=1); sec3.columnconfigure(3, weight=1)

    tk.Label(sec3, text="TOTALS", font=("Helvetica", 9, "bold"),
             bg=BG_CARD, fg=TEXT_GRAY).grid(row=0, column=0, columnspan=4,
             sticky="w", padx=20, pady=(10, 2))
    tk.Frame(sec3, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4,
             sticky="ew", padx=15, pady=(0, 5))

    _label(sec3, "Total Amount (₹)", 2, 2); _styled_entry(sec3, TotalVar, 2, 3)
    _label(sec3, "Cost / GST (%)",   3, 2); _styled_entry(sec3, CostVar,  3, 3)

    tk.Label(sec3, text="Net Bill (₹)", font=("Helvetica", 12, "bold"),
             bg=BG_CARD, fg=ACCENT_GREEN
             ).grid(row=4, column=2, sticky="w", padx=(20, 8), pady=5)
    tk.Entry(sec3, textvariable=NetVar, width=30,
             bg=BG_INPUT, fg=ACCENT_GREEN, insertbackground="white",
             relief="flat", font=("Helvetica", 13, "bold"),
             highlightbackground=ACCENT_GREEN, highlightcolor=ACCENT_GREEN,
             highlightthickness=2
             ).grid(row=4, column=3, sticky="ew", padx=(0, 20), pady=5)

    # ── Save Button ──
    def savedata():
        # — Validate required fields —
        if not Billnovar.get().strip():
            messagebox.showwarning("⚠️ Missing", "Please enter a Bill No before saving.")
            return
        if not CompanyVar.get().strip():
            messagebox.showwarning("⚠️ Missing", "Please select a Company Name before saving.")
            return
        try:
            # Update stock only for rows that have BOTH item and qty filled
            for item, qty in zip(item_vars, qty_vars):
                i_val = item.get().strip()
                q_val = qty.get().strip()
                if i_val and q_val:
                    update_stock_qty(i_val, q_val)

            cur.execute(
                "INSERT INTO Purchase VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (Billnovar.get(), DOBvar.get(), CompanyVar.get(),
                 AddrVar.get(), EmailVar.get(), MobVar.get(),
                 *(v.get() for v in item_vars),
                 *(v.get() for v in price_vars),
                 *(v.get() for v in qty_vars),
                 *(v.get() for v in amt_vars),
                 TotalVar.get(), CostVar.get(), NetVar.get())
            )
            conn.commit()
            messagebox.showinfo("Saved ✅", "Purchase bill saved successfully!")
            # Clear all fields
            for v in [Billnovar, DOBvar, CompanyVar, AddrVar, EmailVar, MobVar,
                      *item_vars, *price_vars, *qty_vars, *amt_vars, TotalVar, NetVar]:
                v.set("")
            CostVar.set("18")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("❌ Save Error", f"Could not save Purchase bill:\n\n{e}")

    save_frame = tk.Frame(container, bg=BG_DARK)
    save_frame.pack(pady=15)
    btn = tk.Button(save_frame, text="💾   SAVE PURCHASE BILL",
                    command=savedata, bg=BTN_SAVE, fg="white",
                    font=("Helvetica", 12, "bold"), relief="flat",
                    cursor="hand2", padx=30, pady=10, bd=0,
                    activebackground=ACCENT_GRN_H, activeforeground="white")
    btn.pack()
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_GRN_H))
    btn.bind("<Leave>", lambda e: btn.config(bg=BTN_SAVE))


# ══════════════════════════════════════════════
#  SALE
# ══════════════════════════════════════════════
def open_sale():
    win = tk.Toplevel()
    win.title("Sale Bill")
    win.configure(bg=BG_DARK)
    win.state("zoomed")
    _build_header(win, "Sale Bill", "💰",
                  subtitle="Record sales to customers  •  Stock auto-reduces on save",
                  accent="#ef4444")

    cur.execute("SELECT Company_Name FROM party WHERE Party_type=?", ("SUNDRY DEBTOR",))
    party_list = [r[0] for r in cur.fetchall()]
    cur.execute("SELECT Item_Name FROM stock")
    stock_list = [r[0] for r in cur.fetchall()]

    def get_party_details(pname):
        cur.execute("SELECT Address,Email,Mobile FROM party WHERE Company_Name=?", (pname,))
        r = cur.fetchall()
        return r[0] if r else ("", "", "")

    def get_price(iname):
        cur.execute("SELECT Price FROM stock WHERE Item_Name=?", (iname,))
        r = cur.fetchone()
        return int(r[0]) if r else 0

    def update_stock_qty(item, qty):
        if item:
            cur.execute("SELECT Opening_item FROM stock WHERE Item_Name=?", (item,))
            r = cur.fetchone()
            if r:
                cur.execute("UPDATE stock SET Opening_item=? WHERE Item_Name=?",
                            (float(r[0]) - float(qty), item))
                conn.commit()

    Billnovar = tk.StringVar(); DOBvar = tk.StringVar()
    CompanyVar = tk.StringVar(); AddrVar = tk.StringVar()
    EmailVar = tk.StringVar(); MobVar = tk.StringVar()
    item_vars = [tk.StringVar() for _ in range(5)]
    price_vars = [tk.StringVar() for _ in range(5)]
    qty_vars = [tk.StringVar() for _ in range(5)]
    amt_vars = [tk.StringVar() for _ in range(5)]
    TotalVar = tk.StringVar(); GSTVar = tk.StringVar(); NetVar = tk.StringVar()
    GSTVar.set("18")

    def calculate(index):
        try:
            p = float(price_vars[index].get() or 0)
            q = int(qty_vars[index].get() or 0)
            amt_vars[index].set(str(p * q))
            total = sum(float(a.get() or 0) for a in amt_vars)
            TotalVar.set(str(total))
            gst = float(GSTVar.get() or 0)
            NetVar.set(str(round(total + total * gst / 100, 2)))
        except Exception as e:
            messagebox.showinfo("Calc Error", str(e))

    canvas = tk.Canvas(win, bg=BG_DARK, highlightthickness=0)
    scroll = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(fill=tk.BOTH, expand=True)
    container = tk.Frame(canvas, bg=BG_DARK)
    canvas.create_window((0, 0), window=container, anchor="nw")
    container.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")))

    sec1 = tk.Frame(container, bg=BG_CARD)
    sec1.pack(fill=tk.X, padx=20, pady=(15, 5))
    sec1.columnconfigure(1, weight=1); sec1.columnconfigure(3, weight=1)

    tk.Label(sec1, text="BILL DETAILS", font=("Helvetica", 9, "bold"),
             bg=BG_CARD, fg=TEXT_GRAY).grid(row=0, column=0, columnspan=4,
             sticky="w", padx=20, pady=(10, 2))
    tk.Frame(sec1, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4,
             sticky="ew", padx=15, pady=(0, 8))

    _label(sec1, "Bill No",       2, 0); _styled_entry(sec1, Billnovar, 2, 1)
    _label(sec1, "Date of Sale",  2, 2); _styled_entry(sec1, DOBvar,    2, 3)
    _label(sec1, "Company Name",  3, 0)
    party_cb = _styled_combobox(sec1, CompanyVar, party_list, 3, 1)
    def on_party(e=None):
        a, m, mob = get_party_details(CompanyVar.get())
        AddrVar.set(a); EmailVar.set(m); MobVar.set(mob)
    party_cb.bind("<<ComboboxSelected>>", on_party)
    _label(sec1, "Address",   4, 0); _styled_entry(sec1, AddrVar,  4, 1)
    _label(sec1, "Email",     5, 0); _styled_entry(sec1, EmailVar, 5, 1)
    _label(sec1, "Mobile No", 5, 2); _styled_entry(sec1, MobVar,   5, 3)

    sec2 = tk.Frame(container, bg=BG_CARD)
    sec2.pack(fill=tk.X, padx=20, pady=5)
    tk.Label(sec2, text="ITEM DETAILS", font=("Helvetica", 9, "bold"),
             bg=BG_CARD, fg=TEXT_GRAY).grid(row=0, column=0, columnspan=4,
             sticky="w", padx=20, pady=(10, 2))
    tk.Frame(sec2, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4,
             sticky="ew", padx=15, pady=(0, 5))
    for col, txt in enumerate(["Item Name", "Price (₹)", "Quantity", "Amount (₹)"]):
        tk.Label(sec2, text=txt, font=("Helvetica", 10, "bold"),
                 bg=BG_CARD, fg="#da3633"
                 ).grid(row=2, column=col, padx=(20 if col==0 else 5, 5), pady=5, sticky="w")

    for i in range(5):
        row_num = 3 + i
        cb = _styled_combobox(sec2, item_vars[i], stock_list, row_num, 0, width=22)
        _styled_entry(sec2, price_vars[i], row_num, 1, width=12)
        qty_cb = _styled_combobox(sec2, qty_vars[i],
                                  [str(n) for n in range(1, 101)], row_num, 2, width=10)
        _styled_entry(sec2, amt_vars[i], row_num, 3, width=12)

        def make_handlers(idx):
            def on_item(e=None):
                price_vars[idx].set(str(get_price(item_vars[idx].get())))
                calculate(idx)
            def on_qty(e=None):
                calculate(idx)
            return on_item, on_qty

        on_item, on_qty = make_handlers(i)
        cb.bind("<<ComboboxSelected>>", on_item)
        qty_cb.bind("<<ComboboxSelected>>", on_qty)

    sec3 = tk.Frame(container, bg=BG_CARD)
    sec3.pack(fill=tk.X, padx=20, pady=5)
    sec3.columnconfigure(1, weight=1); sec3.columnconfigure(3, weight=1)
    tk.Label(sec3, text="TOTALS", font=("Helvetica", 9, "bold"),
             bg=BG_CARD, fg=TEXT_GRAY).grid(row=0, column=0, columnspan=4,
             sticky="w", padx=20, pady=(10, 2))
    tk.Frame(sec3, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4,
             sticky="ew", padx=15, pady=(0, 5))
    _label(sec3, "Total Amount (₹)", 2, 2); _styled_entry(sec3, TotalVar, 2, 3)
    _label(sec3, "GST (%)",          3, 2); _styled_entry(sec3, GSTVar,   3, 3)
    tk.Label(sec3, text="Net Bill (₹)", font=("Helvetica", 12, "bold"),
             bg=BG_CARD, fg="#da3633"
             ).grid(row=4, column=2, sticky="w", padx=(20, 8), pady=5)
    tk.Entry(sec3, textvariable=NetVar, width=30,
             bg=BG_INPUT, fg="#da3633", insertbackground="white",
             relief="flat", font=("Helvetica", 13, "bold"),
             highlightbackground="#da3633", highlightcolor="#da3633",
             highlightthickness=2
             ).grid(row=4, column=3, sticky="ew", padx=(0, 20), pady=5)

    def savedata():
        # — Validate required fields —
        if not Billnovar.get().strip():
            messagebox.showwarning("⚠️ Missing", "Please enter a Bill No before saving.")
            return
        if not CompanyVar.get().strip():
            messagebox.showwarning("⚠️ Missing", "Please select a Company Name before saving.")
            return
        try:
            # Update stock only for rows that have BOTH item and qty filled
            for item, qty in zip(item_vars, qty_vars):
                i_val = item.get().strip()
                q_val = qty.get().strip()
                if i_val and q_val:
                    update_stock_qty(i_val, q_val)

            cur.execute(
                "INSERT INTO sale VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (Billnovar.get(), DOBvar.get(), CompanyVar.get(),
                 AddrVar.get(), EmailVar.get(), MobVar.get(),
                 *(v.get() for v in item_vars),
                 *(v.get() for v in price_vars),
                 *(v.get() for v in qty_vars),
                 *(v.get() for v in amt_vars),
                 TotalVar.get(), GSTVar.get(), NetVar.get())
            )
            conn.commit()
            messagebox.showinfo("Saved ✅", "Sale bill saved successfully!")
            # Clear all fields
            for v in [Billnovar, DOBvar, CompanyVar, AddrVar, EmailVar, MobVar,
                      *item_vars, *price_vars, *qty_vars, *amt_vars, TotalVar, NetVar]:
                v.set("")
            GSTVar.set("18")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("❌ Save Error", f"Could not save Sale bill:\n\n{e}")

    save_frame = tk.Frame(container, bg=BG_DARK)
    save_frame.pack(pady=15)
    btn = tk.Button(save_frame, text="💾   SAVE SALE BILL",
                    command=savedata, bg="#da3633", fg="white",
                    font=("Helvetica", 12, "bold"), relief="flat",
                    cursor="hand2", padx=30, pady=10, bd=0,
                    activebackground=_darken("#da3633"), activeforeground="white")
    btn.pack()
    btn.bind("<Enter>", lambda e: btn.config(bg=_darken("#da3633")))
    btn.bind("<Leave>", lambda e: btn.config(bg="#da3633"))


# ══════════════════════════════════════════════
#  DISPLAY STOCK
# ══════════════════════════════════════════════
def open_display():
    win = tk.Toplevel()
    win.title("Display Stock")
    win.configure(bg=BG_DARK)
    _center_window(win, 860, 600)
    _build_header(win, "Display Stock by Category", "📊",
                  subtitle="Browse current stock levels and prices per category",
                  accent=ACCENT_BLUE)

    top = tk.Frame(win, bg=BG_CARD)
    top.pack(fill=tk.X, padx=20, pady=15)
    top.columnconfigure(1, weight=1)

    cur.execute("SELECT category_Name FROM category")
    cat_list = [r[0] for r in cur.fetchall()]
    categoryVar = tk.StringVar()

    _label(top, "Select Category", 0, 0)
    cb = _styled_combobox(top, categoryVar, cat_list, 0, 1, width=35)

    # Treeview
    tv_frame = tk.Frame(win, bg=BG_DARK)
    tv_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Pro.Treeview",
                    background=BG_CARD, foreground=TEXT_LIGHT,
                    rowheight=30, fieldbackground=BG_CARD,
                    font=("Helvetica", 10))
    style.configure("Pro.Treeview.Heading",
                    background=BG_INPUT, foreground=ACCENT_GREEN,
                    font=("Helvetica", 10, "bold"), relief="flat")
    style.map("Pro.Treeview",
              background=[("selected", ACCENT_GREEN)],
              foreground=[("selected", "white")])

    tree = ttk.Treeview(tv_frame,
                         columns=("Item", "Quantity", "Price"),
                         show="headings", height=18,
                         style="Pro.Treeview")
    tree.heading("Item",     text="📦  Item Name")
    tree.heading("Quantity", text="📦  Stock Qty")
    tree.heading("Price",    text="💰  Price (₹)")
    tree.column("Item",     width=300, anchor="w")
    tree.column("Quantity", width=150, anchor="center")
    tree.column("Price",    width=150, anchor="center")

    vsb = ttk.Scrollbar(tv_frame, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(tv_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side=tk.RIGHT,  fill=tk.Y)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)
    tree.pack(fill=tk.BOTH, expand=True)

    def on_category(event=None):
        for row in tree.get_children():
            tree.delete(row)
        cur.execute("SELECT Item_Name,Opening_item,Price FROM stock WHERE Category=?",
                    (categoryVar.get(),))
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    cb.bind("<<ComboboxSelected>>", on_category)


# ══════════════════════════════════════════════
#  PURCHASE BILL VIEW
# ══════════════════════════════════════════════
def open_purchase_bill():
    win = tk.Toplevel()
    win.title("Purchase Bill Viewer")
    win.configure(bg=BG_DARK)
    _center_window(win, 900, 600)
    _build_header(win, "Purchase Bill Viewer", "🧾", accent="#39d353")

    top = tk.Frame(win, bg=BG_CARD)
    top.pack(fill=tk.X, padx=20, pady=15)

    cur.execute("SELECT Billno FROM Purchase")
    bill_list = [r[0] for r in cur.fetchall()]
    BillVar = tk.StringVar()

    _label(top, "Select Bill No", 0, 0)
    cb = _styled_combobox(top, BillVar, bill_list, 0, 1, width=35)

    tv_frame = tk.Frame(win, bg=BG_DARK)
    tv_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Pro.Treeview",
                    background=BG_CARD, foreground=TEXT_LIGHT,
                    rowheight=30, fieldbackground=BG_CARD,
                    font=("Helvetica", 10))
    style.configure("Pro.Treeview.Heading",
                    background=BG_INPUT, foreground=ACCENT_GREEN,
                    font=("Helvetica", 10, "bold"), relief="flat")
    style.map("Pro.Treeview",
              background=[("selected", ACCENT_GREEN)],
              foreground=[("selected", "white")])

    cols = ("Date", "Company", "Address", "Email", "Mobile", "Total", "Net Bill")
    tree = ttk.Treeview(tv_frame, columns=cols, show="headings",
                         height=18, style="Pro.Treeview")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    vsb = ttk.Scrollbar(tv_frame, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(tv_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side=tk.RIGHT,  fill=tk.Y)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)
    tree.pack(fill=tk.BOTH, expand=True)

    def on_bill(event=None):
        for row in tree.get_children():
            tree.delete(row)
        cur.execute(
            "SELECT DOBpurchase,Company_Name,Address,Email,Mobile,TotalAmount,NetBill FROM Purchase WHERE Billno=?",
            (BillVar.get(),))
        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    cb.bind("<<ComboboxSelected>>", on_bill)


# ══════════════════════════════════════════════════════════
#  DATABASE VIEWER  —  See ALL your data in one place
# ══════════════════════════════════════════════════════════
def open_database_viewer():
    """
    Full-screen tabbed viewer for every table in inventory.db.
    Tabs: Sale | Purchase | Stock | Party | Unit | Category | Godown
    Features: live search, row-count badge, refresh, alternating rows.
    """
    win = tk.Toplevel()
    win.title("Database Viewer — All Records")
    win.configure(bg=BG_DARK)
    win.state("zoomed")
    _build_header(win, "Database Viewer", "🗄️",
                  subtitle="Browse all your saved records  •  Sale • Purchase • Stock • Party • and more",
                  accent=ACCENT_BLUE)

    # ── Table definitions: (tab label, SQL query, column headers) ──────────
    TABS = [
        (
            "💰  Sale",
            "SELECT Billno,DOBsale,Company_Name,Address,Email,Mobile,"
            "Item1,Item2,Item3,Item4,Item5,"
            "Price1,Price2,Price3,Price4,Price5,"
            "Qty1,Qty2,Qty3,Qty4,Qty5,"
            "Amount1,Amount2,Amount3,Amount4,Amount5,"
            "TotalAmount,GST,NetBill FROM sale",
            ["Bill No","Date","Company","Address","Email","Mobile",
             "Item1","Item2","Item3","Item4","Item5",
             "Price1","Price2","Price3","Price4","Price5",
             "Qty1","Qty2","Qty3","Qty4","Qty5",
             "Amt1","Amt2","Amt3","Amt4","Amt5",
             "Total","GST%","Net Bill"],
            "#ef4444",
        ),
        (
            "🛒  Purchase",
            "SELECT Billno,DOBpurchase,Company_Name,Address,Email,Mobile,"
            "Item1,Item2,Item3,Item4,Item5,"
            "Price1,Price2,Price3,Price4,Price5,"
            "Qty1,Qty2,Qty3,Qty4,Qty5,"
            "Amount1,Amount2,Amount3,Amount4,Amount5,"
            "TotalAmount,Cost,NetBill FROM Purchase",
            ["Bill No","Date","Company","Address","Email","Mobile",
             "Item1","Item2","Item3","Item4","Item5",
             "Price1","Price2","Price3","Price4","Price5",
             "Qty1","Qty2","Qty3","Qty4","Qty5",
             "Amt1","Amt2","Amt3","Amt4","Amt5",
             "Total","GST%","Net Bill"],
            ACCENT_GREEN,
        ),
        (
            "📦  Stock",
            "SELECT Item_Name,Unit_Name,category,Opening_item,price,GST_Rate FROM stock",
            ["Item Name","Unit","Category","Stock Qty","Price (₹)","GST %"],
            ACCENT_BLUE,
        ),
        (
            "👥  Party",
            "SELECT Company_Name,Party_type,Address,State,Email,Mobile FROM party",
            ["Company Name","Type","Address","State","Email","Mobile"],
            "#f59e0b",
        ),
        (
            "📏  Unit",
            "SELECT Formal_Name,Full_Name FROM unit",
            ["Formal Name","Full Name"],
            "#8957e5",
        ),
        (
            "🗂️  Category",
            "SELECT category_Name,category_fullName FROM category",
            ["Category Name","Full Name"],
            "#f472b6",
        ),
        (
            "🏭  Godown",
            "SELECT godown_Name,godown_type,Address FROM godown",
            ["Godown Name","Type","Address"],
            "#38bdf8",
        ),
    ]

    # ── Style the Notebook tabs ─────────────────────────────────────────────
    nb_style = ttk.Style()
    nb_style.theme_use("clam")
    nb_style.configure("DB.TNotebook",
                       background=BG_DARK, borderwidth=0, tabmargins=0)
    nb_style.configure("DB.TNotebook.Tab",
                       background=BG_CARD2, foreground=TEXT_GRAY,
                       font=("Helvetica", 10, "bold"),
                       padding=[16, 8], borderwidth=0)
    nb_style.map("DB.TNotebook.Tab",
                 background=[("selected", BG_CARD)],
                 foreground=[("selected", TEXT_WHITE)])

    # ── Top toolbar (search + refresh + count) ──────────────────────────────
    toolbar = tk.Frame(win, bg=BG_CARD2, height=52)
    toolbar.pack(fill=tk.X, padx=0, pady=0)
    toolbar.pack_propagate(False)

    tk.Frame(toolbar, bg=BORDER, height=1).pack(fill=tk.X, side=tk.BOTTOM)

    # Search label + entry
    tk.Label(toolbar, text="🔍  Search:", font=("Helvetica", 10),
             bg=BG_CARD2, fg=TEXT_LIGHT).pack(side=tk.LEFT, padx=(18, 4), pady=14)

    search_var = tk.StringVar()
    search_entry = tk.Entry(toolbar, textvariable=search_var,
                            bg=BG_INPUT, fg=TEXT_WHITE,
                            insertbackground=ACCENT_GREEN,
                            relief="flat", font=("Helvetica", 11), width=28,
                            highlightbackground=BORDER_GLOW,
                            highlightcolor=ACCENT_GREEN, highlightthickness=1)
    search_entry.pack(side=tk.LEFT, pady=14, ipady=4)
    search_entry.bind("<FocusIn>",
                      lambda e: search_entry.config(highlightbackground=ACCENT_GREEN,
                                                    highlightthickness=2))
    search_entry.bind("<FocusOut>",
                      lambda e: search_entry.config(highlightbackground=BORDER_GLOW,
                                                    highlightthickness=1))

    # Row count badge
    count_var = tk.StringVar(value="0 rows")
    count_lbl = tk.Label(toolbar, textvariable=count_var,
                         font=("Helvetica", 9, "bold"),
                         bg=ACCENT_BLUE, fg="white",
                         padx=10, pady=3)
    count_lbl.pack(side=tk.LEFT, padx=14, pady=16)

    # Refresh button
    def refresh_current():
        _load_tab(notebook.index(notebook.select()))

    ref_btn = tk.Button(toolbar, text="🔄  Refresh",
                        command=refresh_current,
                        bg=BG_CARD, fg=TEXT_LIGHT,
                        font=("Helvetica", 9, "bold"),
                        relief="flat", cursor="hand2",
                        padx=14, pady=5, bd=0,
                        activebackground=BG_HOVER,
                        activeforeground=TEXT_WHITE)
    ref_btn.pack(side=tk.LEFT, padx=4, pady=16)
    ref_btn.bind("<Enter>", lambda e: ref_btn.config(bg=BG_HOVER))
    ref_btn.bind("<Leave>", lambda e: ref_btn.config(bg=BG_CARD))

    # Hint label on right
    tk.Label(toolbar, text="Tip: Type in Search to filter any column instantly",
             font=("Helvetica", 8, "italic"),
             bg=BG_CARD2, fg=TEXT_GRAY).pack(side=tk.RIGHT, padx=20)

    # ── Notebook ────────────────────────────────────────────────────────────
    notebook = ttk.Notebook(win, style="DB.TNotebook")
    notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

    # Keep references per tab: { tab_index: (tree, all_rows, columns) }
    tab_data = {}

    def _make_treeview(parent, columns, accent):
        """Build a styled Treeview with scrollbars inside parent frame."""
        tv_style = ttk.Style()
        tv_style.theme_use("clam")
        style_name = f"Tab{accent}.Treeview"
        tv_style.configure(style_name,
                           background=BG_CARD,
                           foreground=TEXT_LIGHT,
                           rowheight=30,
                           fieldbackground=BG_CARD,
                           font=("Helvetica", 10))
        tv_style.configure(f"{style_name}.Heading",
                           background=BG_CARD2,
                           foreground=accent,
                           font=("Helvetica", 10, "bold"),
                           relief="flat")
        tv_style.map(style_name,
                     background=[("selected", accent)],
                     foreground=[("selected", "white")])

        frame = tk.Frame(parent, bg=BG_DARK)
        frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(frame, orient="vertical")
        hsb = ttk.Scrollbar(frame, orient="horizontal")
        tree = ttk.Treeview(frame, columns=columns, show="headings",
                            yscrollcommand=vsb.set, xscrollcommand=hsb.set,
                            style=style_name)

        for col in columns:
            # Wider for long columns, narrow for short ones
            w = 180 if len(col) > 8 else (100 if len(col) > 4 else 70)
            tree.heading(col, text=col,
                         command=lambda c=col, t=tree: _sort_column(t, c))
            tree.column(col, width=w, anchor="center", minwidth=60)

        # Tag for alternating rows
        tree.tag_configure("odd",  background=BG_CARD)
        tree.tag_configure("even", background=BG_CARD2)

        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(fill=tk.BOTH, expand=True)
        return tree

    def _sort_column(tree, col):
        """Sort treeview by clicking a column header."""
        data = [(tree.set(child, col), child)
                for child in tree.get_children("")]
        try:
            data.sort(key=lambda x: float(x[0]) if x[0] else 0)
        except ValueError:
            data.sort(key=lambda x: x[0].lower())
        for idx, (_, child) in enumerate(data):
            tree.move(child, "", idx)
            tree.item(child, tags=("even" if idx % 2 == 0 else "odd",))

    def _load_tab(idx):
        """Fetch data from DB and populate the correct tab's treeview."""
        if idx not in tab_data:
            return
        tree, sql, cols = tab_data[idx]

        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)

        # Fetch all rows
        try:
            cur.execute(sql)
            rows = cur.fetchall()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
            return

        # Apply search filter
        q = search_var.get().strip().lower()
        filtered = rows
        if q:
            filtered = [r for r in rows
                        if any(q in str(cell).lower() for cell in r)]

        # Insert with alternating colours
        for i, row in enumerate(filtered):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", tk.END, values=row, tags=(tag,))

        count_var.set(f"{len(filtered)} / {len(rows)} rows")

    # ── Build one tab per table ──────────────────────────────────────────────
    for i, (tab_label, sql, cols, accent) in enumerate(TABS):
        tab_frame = tk.Frame(notebook, bg=BG_DARK)
        notebook.add(tab_frame, text=f"  {tab_label}  ")

        # Coloured top stripe on each tab page
        tk.Frame(tab_frame, bg=accent, height=3).pack(fill=tk.X)

        tree = _make_treeview(tab_frame, cols, accent)
        tab_data[i] = (tree, sql, cols)

    # ── Live search: re-filter on every keystroke ───────────────────────────
    def _on_search(*_):
        _load_tab(notebook.index(notebook.select()))

    search_var.trace_add("write", _on_search)

    # ── Reload data when switching tabs ─────────────────────────────────────
    def _on_tab_change(event):
        search_var.set("")          # clear search on tab switch
        _load_tab(notebook.index(notebook.select()))

    notebook.bind("<<NotebookTabChanged>>", _on_tab_change)

    # ── Load first tab on open ───────────────────────────────────────────────
    win.after(100, lambda: _load_tab(0))
