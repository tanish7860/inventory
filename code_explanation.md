# 📦 INVENTORY SYSTEM — SUPER EASY CODE EXPLANATION
### Files: `front_page.py` + `windows.py`
### ✅ Written so YOU can understand it easily — with real examples!

---

## 🗺️ BIG PICTURE — How the App Works

```
You run front_page.py
        ↓
Dashboard opens (the main screen you see)
        ↓
You click a button (Unit / Stock / Category / etc.)
        ↓
A popup window opens (from windows.py)
        ↓
You fill in the form and click Save / Search / Delete / Update
        ↓
The data goes to / comes from inventory.db (your database file)
```

---

## 🖥️ PART 1 — front_page.py (The Dashboard / Home Screen)

This file builds the **main window** you see when the app starts.

### What you see on screen:

```
┌─────────────────────────────────────────────────────────┐
│  📦 INVENTORY PRO   Smart Inventory. Real Results.  🕐  │  ← TOP BAR
├──────────────┬──────────────────────────────────────────┤
│  NAVIGATION  │  Inventory Management System             │
│              │  ────────────────────────────────────    │
│  👥 Party    │  LIVE STATISTICS                         │
│  🛒 Purchase │  [📦 5] [🗂️ 3] [👥 10] [🛒 2] [💰 7] [📏 4] │
│  💰 Sale     │  ────────────────────────────────────    │
│  📊 Reports  │  MODULES — Click to open                 │
│  🏭 Godown   │  [Unit][Stock][Category][Godown]...      │
│              │  ────────────────────────────────────    │
│  ● DB Connected│ [🚀 OPEN FULL APP]  [🔄 Refresh Stats] │
└──────────────┴──────────────────────────────────────────┘
│  ● Ready | Inventory Management System v1.0              │  ← STATUS BAR
└─────────────────────────────────────────────────────────┘
```

---

### 📌 What each button does on the Dashboard:

| Button | What happens when you click it |
|--------|-------------------------------|
| 📏 **Unit Measure** | Opens Unit window (to add/edit units like KG, Liter) |
| 📦 **Stock Items** | Opens Stock window (to add items like Sugar, Rice) |
| 🗂️ **Category** | Opens Category window (to group items like Food, Electronics) |
| 🏭 **Godown** | Opens Godown window (to add warehouse locations) |
| 👥 **Party Details** | Opens Party window (to add customers/suppliers) |
| 🛒 **Purchase Bill** | Opens Purchase form (to record buying from supplier) |
| 💰 **Sale Bill** | Opens Sale form (to record selling to customer) |
| 📊 **Display Stock** | Opens stock viewer (to see items by category) |
| 🚀 **Open Full App** | Launches the old plain.py app |
| 🔄 **Refresh Stats** | Updates the live number cards at the top |

---

### 🔴 Live Statistics Cards — How they work:

```python
def _fetch_stats(self):
    # Goes to database and counts rows in each table
    "SELECT COUNT(*) FROM stock"      → counts stock items
    "SELECT COUNT(*) FROM category"   → counts categories
    "SELECT COUNT(*) FROM party"      → counts parties
    "SELECT COUNT(*) FROM Purchase"   → counts purchases
    "SELECT COUNT(*) FROM sale"       → counts sales
    "SELECT COUNT(*) FROM unit"       → counts units
```

👉 Every time you click **🔄 Refresh Stats**, this runs and updates the numbers you see.

---

## 🪟 PART 2 — windows.py (All the Popup Windows)

This file has **one function for each popup window**.

Every window has the **same 5 buttons**: Save, Search, Delete, Update, Clear.

---

## 📏 WINDOW 1 — Unit of Measure (open_unit)

**Purpose:** Add measuring units like KG, Liter, Piece, Dozen, etc.

**Fields:**
```
Formal Name:  [ KG        ]    ← Short name (like abbreviation)
Full Name:    [ Kilogram  ]    ← Full name
```

### What happens when you click each button:

#### 💾 SAVE button

```
You type:
   Formal Name = "kg"
   Full Name   = "kilogram"
          ↓
savedata() runs
          ↓
Text is converted to UPPERCASE → "KG", "KILOGRAM"
          ↓
SQL runs: INSERT INTO unit VALUES("KG", "KILOGRAM")
          ↓
conn.commit() → data saved to database
          ↓
Popup shows: "Unit saved successfully! ✅"
          ↓
Fields are cleared automatically
```

#### 🔍 SEARCH button

```
You type:
   Formal Name = "kg"
          ↓
searchdata() runs
          ↓
SQL runs: SELECT * FROM unit WHERE Formal_Name = "KG"
          ↓
If found → Full Name field fills automatically with "KILOGRAM"
If NOT found → Popup shows: "No record found."
```

#### 🗑️ DELETE button

```
You type:
   Formal Name = "kg"
          ↓
deletedata() runs
          ↓
SQL runs: DELETE FROM unit WHERE Formal_Name = "KG"
          ↓
conn.commit() → deletion saved
          ↓
Popup shows: "Record deleted. 🗑️"
          ↓
Fields are cleared
```

#### ✏️ UPDATE button

```
You first SEARCH for "kg" (so Full Name fills in)
Then you change Full Name to "Kilogram (KG)"
Then click UPDATE
          ↓
updatedata() runs
          ↓
SQL runs: UPDATE unit SET Full_Name="KILOGRAM (KG)" WHERE Formal_Name="KG"
          ↓
conn.commit() → change saved
          ↓
Popup shows: "Record updated. ✏️"
```

#### ✖ CLEAR button

```
cleardata() runs
          ↓
Both fields are set to "" (empty)
          ↓
Form is blank again — ready for new entry
```

---

## 📦 WINDOW 2 — Stock Items (open_stock)

**Purpose:** Add items you sell/buy (Sugar, Rice, Oil, etc.)

**Fields:**
```
Item Name:     [ Sugar       ]
Unit Name:     [ KG    ▼    ]   ← Dropdown (from unit table)
Category:      [ Food  ▼    ]   ← Dropdown (from category table)
Opening Stock: [ 100         ]   ← How many you have now
Price (₹):     [ 50          ]
GST Rate (%):  [ 18          ]
```

Note: Unit and Category dropdowns load from the database!

### 💾 SAVE button flow:

```
Fill all 6 fields → Click Save
          ↓
savedata() runs
          ↓
try:
    INSERT INTO stock VALUES("SUGAR", "KG", "FOOD", 100, 50, 18)
    conn.commit()
    Show: "Stock item saved! ✅"
    Clear all fields
except:
    If something goes wrong (like duplicate item name)
    Show: Error message
```

### 🔍 SEARCH button flow:

```
Type Item Name = "sugar" → Click Search
          ↓
SELECT * FROM stock WHERE Item_Name = "SUGAR"
          ↓
All fields auto-fill:
   Unit Name     → KG
   Category      → FOOD
   Opening Stock → 100
   Price         → 50
   GST Rate      → 18
```

---

## 🗂️ WINDOW 3 — Category (open_category)

**Purpose:** Create groups for your items (Food, Electronics, Clothing, etc.)

**Fields:**
```
Category Name:      [ FOOD  ]
Category Full Name: [ Food Products ]
```

Same 5 buttons → Same pattern as Unit window (Save/Search/Delete/Update/Clear)

---

## 🏭 WINDOW 4 — Godown / Warehouse (open_godown)

**Purpose:** Add warehouse/storage locations

**Fields:**
```
Godown Name: [ MAIN WAREHOUSE ]
Godown Type: [ COLD STORAGE   ]
Address:     [ Plot 5, Indore  ]
```

Same 5 buttons → Same pattern

---

## 👥 WINDOW 5 — Party Details (open_party)

**Purpose:** Add your suppliers (who you buy from) and customers (who you sell to)

**Fields:**
```
Company Name: [ ABC Traders          ]
Party Type:   [ Sundry Creditor ▼   ]  ← Dropdown with 2 choices
Address:      [ 123 Main Street      ]
State:        [ Madhya Pradesh       ]
Email:        [ abc@gmail.com        ]
Mobile:       [ 9876543210           ]
```

### What is Party Type?

```
Sundry CREDITOR = Supplier (someone YOU buy FROM)
                  → Appears in Purchase Bill dropdown

Sundry DEBTOR   = Customer (someone who buys FROM YOU)
                  → Appears in Sale Bill dropdown
```

---

## 🛒 WINDOW 6 — Purchase Bill (open_Purchase)

**Purpose:** Record when you BUY items from a supplier

**What the screen looks like:**
```
┌─ BILL DETAILS ──────────────────────────────────┐
│ Bill No:  [001]     Date of Purchase: [13/08/26] │
│ Company:  [ABC Traders ▼]  (Sundry Creditors)    │
│ Address:  [Auto-fills!]                           │
│ Email:    [Auto-fills!]    Mobile: [Auto-fills!] │
└──────────────────────────────────────────────────┘
┌─ ITEM DETAILS ──────────────────────────────────┐
│ Item Name    │ Price(₹) │ Quantity │ Amount(₹)  │
│ [Sugar   ▼]  │ [50]     │ [10 ▼]  │ [500]      │  ← Auto calc!
│ [Rice    ▼]  │ [40]     │ [5  ▼]  │ [200]      │  ← Auto calc!
│ ...5 rows...                                     │
└──────────────────────────────────────────────────┘
┌─ TOTALS ────────────────────────────────────────┐
│ Total Amount: [700]                              │
│ Cost / GST %: [18]                               │
│ Net Bill:     [826.00]  ← Total + GST            │
└──────────────────────────────────────────────────┘
              [💾 SAVE PURCHASE BILL]
```

### Smart Auto-fill Features:

#### When you select a Company from dropdown:

```
on_party() runs automatically
          ↓
SELECT Address, Email, Mobile FROM party WHERE Company_Name = "ABC TRADERS"
          ↓
Address, Email, Mobile fields fill automatically!
```

#### When you select an Item from dropdown:

```
on_item() runs automatically
          ↓
SELECT Price FROM stock WHERE Item_Name = "SUGAR"
          ↓
Price field fills with "50" automatically!
```

#### When you select a Quantity from dropdown:

```
on_qty() runs automatically
          ↓
calculate() runs
          ↓
Amount   = Price × Quantity  →  50 × 10 = 500
Total    = Sum of all amounts → 500 + 200 = 700
Net Bill = Total + Total×GST% → 700 + 700×18/100 = 826.00
          ↓
All these fields update INSTANTLY!
```

### 💾 SAVE PURCHASE BILL button:

```
Click Save
          ↓
savedata() runs
          ↓
STEP 1: Update stock quantities (INCREASE because you bought!)
   Sugar: old stock = 50, bought 10 → new stock = 60
   Rice:  old stock = 20, bought 5  → new stock = 25

STEP 2: Save full bill to Purchase table (29 columns!)
   INSERT INTO Purchase VALUES(
     "001",          ← Bill No
     "13/08/2026",   ← Date
     "ABC TRADERS",  ← Company
     "123 Main St",  ← Address
     ...             ← All item names, prices, qtys, amounts
     700, 18, 826.00 ← Total, GST%, Net Bill
   )

STEP 3: Show "Purchase bill saved! ✅"
STEP 4: Clear all fields, reset GST to 18
```

---

## 💰 WINDOW 7 — Sale Bill (open_sale)

**Purpose:** Record when you SELL items to a customer

Almost exactly like Purchase Bill! Key differences:

| Feature | Purchase | Sale |
|---------|----------|------|
| Party dropdown | Only Sundry **CREDITOR** | Only Sundry **DEBTOR** |
| Stock change | **INCREASES** (+) buying | **DECREASES** (-) selling |
| Tax field name | Cost / GST % | GST % |
| Saved to table | Purchase | sale |
| Header color | Green | Red |

### Stock update on Sale:

```
You sell 10 KG Sugar
          ↓
update_stock_qty("SUGAR", 10) runs
          ↓
Old stock = 60
New stock = 60 - 10 = 50   ← SUBTRACTED!
          ↓
UPDATE stock SET Opening_item = 50 WHERE Item_Name = "SUGAR"
```

---

## 📊 WINDOW 8 — Display Stock (open_display)

**Purpose:** View your current stock levels sorted by category

**How it works:**
```
Select Category: [Food ▼]
          ↓
on_category() runs
          ↓
Old table rows are deleted first (to refresh)
          ↓
SELECT Item_Name, Opening_item, Price FROM stock WHERE Category = "FOOD"
          ↓
Results appear in the table:
┌──────────────┬───────────┬────────────┐
│ Item Name    │ Stock Qty │ Price (₹)  │
├──────────────┼───────────┼────────────┤
│ SUGAR        │ 50        │ 50         │
│ RICE         │ 25        │ 40         │
│ OIL          │ 10        │ 120        │
└──────────────┴───────────┴────────────┘
```

---

## 🧠 KEY CODE CONCEPTS (Simple Explanations)

### 1️⃣ StringVar — The live link between your code and the form

```python
Formal_Namevar = tk.StringVar()
```
Think of it like a **live sticky note** that is glued to the text box.
- When user types → the sticky note updates
- When code sets it → the text box updates

```python
Formal_Namevar.get()    # Read what is on the sticky note
Formal_Namevar.set("")  # Erase the sticky note
```

---

### 2️⃣ conn and cur — Your database pen and paper

```python
conn = sqlite3.connect("inventory.db")  # Open the database file
cur  = conn.cursor()                    # Get a "pen" to write/read
```

| Code | What it does |
|------|-------------|
| `cur.execute("SELECT ...")` | Ask a question to the database |
| `cur.fetchone()` | Get 1 answer |
| `cur.fetchall()` | Get ALL answers |
| `conn.commit()` | Save/confirm changes permanently |

---

### 3️⃣ SQL Commands — 4 things you can do with data

```
INSERT → Add new record        (Save button)
SELECT → Read/find record      (Search button)
DELETE → Remove record         (Delete button)
UPDATE → Change existing data  (Update button)
```

The `?` in SQL is a safe placeholder:
```python
cur.execute("SELECT * FROM unit WHERE Formal_Name=?", ("KG",))
#                                                  ↑
#                                        ? gets replaced by "KG"
```

---

### 4️⃣ Combobox — The dropdown menu

```python
_styled_combobox(form, Unit_Namevar, unit_list, row=2, col=1)
```
- `unit_list` = the options shown in dropdown
- `Unit_Namevar` = stores whatever the user picks
- `.bind("<<ComboboxSelected>>", function)` = when user picks something, run this function

---

### 5️⃣ try-except — Protection against crashes

```python
try:
    cur.execute("INSERT INTO stock VALUES(?,?,?,?,?,?)", (...))
    conn.commit()
except Exception as e:
    messagebox.showerror("Error", str(e))
```

**Without try-except:** If something goes wrong, the whole app crashes.
**With try-except:** If something goes wrong, show a nice error message instead. ✅

---

### 6️⃣ .bind() — Connects an action to a function

```python
party_cb.bind("<<ComboboxSelected>>", on_party)
```
This means: **"When user selects from party dropdown → run on_party() function"**

Other events you will see:

| Event | When it happens |
|-------|----------------|
| `"<Button-1>"` | Left mouse click |
| `"<Enter>"` | Mouse hovers over widget |
| `"<Leave>"` | Mouse moves away from widget |
| `"<<ComboboxSelected>>"` | User picks from dropdown |

---

## 🗄️ DATABASE TABLES SUMMARY

All your data is stored in `inventory.db` — these are your tables:

| Table | What it stores | Columns |
|-------|---------------|---------|
| `unit` | Measuring units | Formal_Name, Full_Name |
| `category` | Item categories | category_Name, category_fullName |
| `godown` | Warehouses | godown_Name, godown_type, Address |
| `party` | Customers and Suppliers | Company_Name, Party_type, Address, State, Email, Mobile |
| `stock` | Inventory items | Item_Name, Unit_Name, category, Opening_item, price, GST_Rate |
| `Purchase` | Purchase bills | Billno, Date, Company, 5 items+prices+qtys+amounts, Total, GST, Net |
| `sale` | Sale bills | Billno, Date, Company, 5 items+prices+qtys+amounts, Total, GST, Net |

---

## 🔄 COMPLETE FLOW EXAMPLE

**Scenario: You buy 20 KG of Sugar from ABC Traders**

```
Step 1: Go to Purchase Bill
Step 2: Bill No = 001, Date = 13/08/2026
Step 3: Select Company = ABC Traders
          → Address, Email, Mobile fill automatically!
Step 4: Select Item 1 = SUGAR
          → Price fills automatically (e.g. 50)
Step 5: Select Quantity = 20
          → Amount = 50 × 20 = 1000  (auto-calculated!)
          → Total = 1000
          → Net Bill = 1000 + 18% = 1180.00
Step 6: Click SAVE PURCHASE BILL
          → Sugar stock: 50 → 70 (increased by 20)
          → Bill saved to Purchase table
          → "Saved ✅" message shown
          → Form cleared
```

---

## 🎨 COLORS USED IN THE APP

| Color Name | Hex Code | Used For |
|-----------|----------|---------|
| Dark background | #0d1117 | Main window bg |
| Card background | #161b22 | Form/card areas |
| Input background | #21262d | Text entry boxes |
| Green accent | #0b9e37 | Save button, Unit window |
| Blue accent | #1f6feb | Search button, Category |
| Red button | #da3633 | Delete button, Sale |
| Yellow button | #d29922 | Update button |
| Gray button | #6e7681 | Clear button |

---

*📌 This file is ONLY for learning. Your actual code is in front_page.py and windows.py.*
*✅ No code was changed — this is just explanation!*
