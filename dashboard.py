import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, date
import requests
import csv
from tkinter import messagebox
from tkinter import filedialog
from pymongo import MongoClient
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog
import math


OPENROUTER_API_KEY = "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"
# Safely extract email from arguments or fallback (during dev/test)
if len(sys.argv) > 1:
    user_email = sys.argv[1]
else:
    user_email = "test@example.com"  # 🔁 You can replace with a valid test email from your DB


client = MongoClient("mongodb://localhost:27017/")
db = client["smartfinance"]
dashboard_col = db["dashboard"]

# Get logged-in user email from login.py

# Fetch user-specific dashboard data
user_data = dashboard_col.find_one({"email": user_email})

if not user_data:
    raise Exception(f"No dashboard data found for {user_email}")
# Appearance and Theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.geometry("1280x720")
root.title("SmartFinance Dashboard")
root.configure(bg="#D3ECCD")  # light green background

# === Fonts ===
title_font = ctk.CTkFont("Gotham-Bold", 24)
card_font = ctk.CTkFont("Gotham-Bold", 18)
text_font = ctk.CTkFont("Gotham-Bold", 16)

# === Sidebar ===
sidebar = ctk.CTkFrame(root, width=200, corner_radius=0, fg_color="#FFFFFF")
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(sidebar, text="SmartFinance 💸", font=title_font, text_color="#06923E").pack(pady=20)
# 👇 Put this AFTER root = ctk.CTk() and sidebar setup

# === Header Cards ===
header = ctk.CTkFrame(root, fg_color="#D3ECCD")  # Light green header background
header.pack(fill="x", padx=30, pady=10)


# === Header Card Creator ===
def create_card(parent, title, amount, color):
    card = ctk.CTkFrame(parent, fg_color=color, width=250, height=80, corner_radius=10)
    card.pack(side="left", padx=15)
    ctk.CTkLabel(card, text=title, font=card_font, text_color="white").pack(anchor="w", padx=10, pady=5)
    label = ctk.CTkLabel(card, text=f"₹ {amount}", font=card_font, text_color="white")
    label.pack(anchor="w", padx=10)
    return label  # ✅ Return for updating later


total_balance_label = create_card(header, "Total Balance", "0", "#045B27")       # Dark green
monthly_expense_label = create_card(header, "Monthly Expenses", "0", "#D64545")  # Red
savings_label = create_card(header, "Savings", "0", "#06923E")                   # Primary green





# === Charts Setup ===
fig1 = plt.Figure(figsize=(3.8, 2.2), dpi=100)
ax1 = fig1.add_subplot(111)
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.get_tk_widget().place(x=700, y=100)

fig2 = plt.Figure(figsize=(3.8, 2.2), dpi=100)
ax2 = fig2.add_subplot(111)
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.get_tk_widget().place(x=700, y=340)

fig3 = plt.Figure(figsize=(3.8, 2.2), dpi=100)
ax3 = fig3.add_subplot(111)
canvas3 = FigureCanvasTkAgg(fig3, master=root)
canvas3.get_tk_widget().place(x=700, y=580)

# === Graph Section (Dynamic) ===
chart_area = ctk.CTkFrame(root, fg_color="#D3ECCD")
chart_area.pack(fill="both", expand=True, padx=20, pady=10)


fund_label = ctk.CTkLabel(root, text="💰 Funds: ₹0", font=card_font, text_color="#045B27")
fund_label.lift()
fund_label.place(x=280, y=120)

sub_label = ctk.CTkLabel(root, text="📦 Subscriptions: 0", font=card_font, text_color="#045B27")
sub_label.place(x=280, y=160)

goal_label = ctk.CTkLabel(root, text="🎯 Goals: 0", font=card_font, text_color="#045B27")
goal_label.place(x=280, y=200)
# ✅ Missing Labels Added Now
# total_balance_label = ctk.CTkLabel(root, text="₹ 0", font=card_font, text_color="#045B27")
# total_balance_label.place(x=250, y=200)

# monthly_expense_label = ctk.CTkLabel(root, text="₹ 0", font=card_font, text_color="#8B0000")
# monthly_expense_label.place(x=250, y=240)

# savings_label = ctk.CTkLabel(root, text="₹ 0", font=card_font, text_color="#006400")
# savings_label.place(x=250, y=280)


# === Emergency Fund Tracker Window (Theme Matched) ===


def auto_refresh():
    refresh_dashboard()
    root.after(5000, auto_refresh) 


def refresh_dashboard():
    global user_data
    user_data = dashboard_col.find_one({"email": user_email})

    # === 1. Default Safe UI ===
    goals = user_data.get("goals", []) if user_data else []
    subscriptions = user_data.get("subscriptions", []) if user_data else []
    history = user_data.get("history", []) if user_data else []

    fund_data = user_data.get("funds", {})
    funds = fund_data.get("saved", 0) if isinstance(fund_data, dict) else fund_data

    # Sidebar cards
    goal_label.configure(text=f"🎯 Goals: {len(goals)}")
    fund_label.configure(text=f"💰 Funds: ₹{funds}")
    sub_label.configure(text=f"📦 Subscriptions: {len(subscriptions)}")

    # === 2. Monthly Calculations ===
    this_month = datetime.now().strftime("%Y-%m")
    monthly_expense = 0
    for h in history:
        if "amount" in h and "date" in h:
            if h["date"].startswith(this_month):
                monthly_expense += h["amount"]

    try:
        expenses = float(monthly_expense)
    except:
        expenses = 0.0

    try:
        savings = float(funds - monthly_expense)
    except:
        savings = 0.0

    # === ✅ Update Header Cards
    total_balance_label.configure(text=f"₹ {funds}")
    monthly_expense_label.configure(text=f"₹ {monthly_expense}")
    savings_label.configure(text=f"₹ {funds - monthly_expense}")

    # === 3. Line Chart - Financial Growth ===
    growth = user_data.get("growth", [0, 0, 0, 0, funds])
    months = ["Jan", "Feb", "Mar", "Apr", "May"]
    ax1.clear()
    ax1.plot(months, growth, marker='o', color="#06923E", linewidth=2)
    ax1.set_title("Financial Growth", fontsize=12)
    ax1.set_facecolor("#F6FFF3")
    canvas1.draw()

    # === 4. Pie Chart - Spending Breakdown ===
    ax2.clear()
    if all(map(lambda x: not math.isnan(x) and x >= 0, [expenses, savings])) and (expenses + savings) > 0:
        ax2.pie([expenses, savings],
                labels=["Expenses", "Savings"],
                colors=["#D64545", "#06923E"],
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "white"})
    else:
        ax2.text(0, 0, "No Data", ha='center', va='center', fontsize=12, color='gray')
    ax2.set_title("Spending", fontsize=11)

    # === 5. Pie Chart - Category Breakdown ===
    ax3.clear()
    category_totals = {}
    for h in history:
        cat = h.get("category", "Others")
        category_totals[cat] = category_totals.get(cat, 0) + h.get("amount", 0)

    if category_totals:
        labels = list(category_totals.keys())
        values = list(category_totals.values())
        colors = plt.cm.Pastel1.colors[:len(labels)]
        ax3.pie(values,
                labels=labels,
                autopct="%1.1f%%",
                colors=colors,
                startangle=140,
                wedgeprops={"edgecolor": "white"})
    else:
        ax3.text(0, 0, "No Data", ha='center', va='center', fontsize=12, color='gray')
    ax3.set_title("Category Breakdown", fontsize=11)

    canvas2.draw()





   

    # Update your pie or line charts here too using matplotlib, etc.
     # Refresh every 5 seconds

 # Start auto-refresh loop
def open_emergency_fund():
    fund_win = ctk.CTkToplevel()
    fund_win.title("Emergency Fund Tracker")
    fund_win.geometry("450x500")
    fund_win.configure(fg_color="#FFFFFF")
    fund_win.attributes("-topmost", True)

    # === Fonts ===
    title_font = ctk.CTkFont(family="Gotham-Bold", size=28)
    text_font = ctk.CTkFont(family="Gotham-Bold", size=18)
    card_font = ctk.CTkFont(family="Gotham-Bold", size=20)

    # === Title ===
    ctk.CTkLabel(fund_win, text="Emergency Fund Tracker", font=title_font, text_color="#06923E").pack(pady=20)

    # === Entry Fields with Placeholders ===
    target_entry = ctk.CTkEntry(fund_win, placeholder_text="Enter Target Amount (₹)", font=text_font, width=300,
                                fg_color="white", border_color="#06923E", text_color="#045B27")
    target_entry.pack(pady=8)

    saved_entry = ctk.CTkEntry(fund_win, placeholder_text="Enter Saved Amount (₹)", font=text_font, width=300,
                               fg_color="white", border_color="#06923E", text_color="#045B27")
    saved_entry.pack(pady=8)

    months_entry = ctk.CTkEntry(fund_win, placeholder_text="Months to Reach Goal", font=text_font, width=300,
                                 fg_color="white", border_color="#06923E", text_color="#045B27")
    months_entry.pack(pady=8)

    # === Output Widgets ===
    progress_label = ctk.CTkLabel(fund_win, text="", font=card_font, text_color="#045B27")
    progress_label.pack(pady=8)

    progress_bar = ctk.CTkProgressBar(fund_win, width=300, progress_color="#06923E")
    progress_bar.pack(pady=10)
    progress_bar.set(0)

    suggestion_label = ctk.CTkLabel(fund_win, text="", font=text_font, text_color="#D64545")
    suggestion_label.pack(pady=8)

    # === Load Existing Fund Data from DB ===
    user_data = dashboard_col.find_one({"email": user_email})
    fund_data = user_data.get("funds", {}) if user_data else {}

    if not isinstance(fund_data, dict):
        fund_data = {}

    saved = str(fund_data.get("saved", ""))
    target = str(fund_data.get("target", ""))
    months = str(fund_data.get("months", ""))

    # ✅ Insert if not empty — else placeholder remains
    if target.strip() != "":
        target_entry.insert(0, target)

    if saved.strip() != "":
        saved_entry.insert(0, saved)

    if months.strip() != "":
        months_entry.insert(0, months)

    # === Show Progress if Valid Data ===
    try:
        saved_val = float(saved)
        target_val = float(target)
        months_val = int(months)

        if target_val > 0 and saved_val >= 0 and months_val > 0:
            ratio = min(saved_val / target_val, 1)
            progress_bar.set(ratio)
            percent = int(ratio * 100)
            progress_label.configure(text=f"Saved ₹{saved_val} / ₹{target_val}  ({percent}%)")

            remaining = max(target_val - saved_val, 0)
            per_month = remaining / months_val
            suggestion_label.configure(
                text=f"📆 Save ₹{per_month:.2f} per month to reach in {months_val} months.", text_color="#045B27")
    except:
        pass

    # === Reset Button (Initially Hidden) ===
    reset_btn = ctk.CTkButton(fund_win, text="Reset Goal", font=text_font,
                              fg_color="#D64545", hover_color="#B33333",
                              text_color="#FFFFFF", command=lambda: reset_goal())
    reset_btn.pack_forget()

    # === Reset Function ===
    def reset_goal():
        # Clear from MongoDB
        dashboard_col.update_one(
            {"email": user_email},
            {"$unset": {"funds": ""}}
        )

        # Clear entry fields (placeholder will show again)
        saved_entry.delete(0, "end")
        target_entry.delete(0, "end")
        months_entry.delete(0, "end")

        # Reset visuals
        progress_label.configure(text="")
        progress_bar.set(0)
        suggestion_label.configure(text="")

        # Hide reset button
        reset_btn.pack_forget()

    # === Show Reset Button if Goal Complete ===
    try:
        if float(saved) == float(target) and float(saved) > 0:
            reset_btn.pack(pady=10)
    except:
        pass

    # === Update Progress ===
    def calculate_progress():
        try:
            target = float(target_entry.get())
            saved = float(saved_entry.get())
            months = int(months_entry.get())

            if target > 0 and saved >= 0 and months > 0:
                ratio = min(saved / target, 1)
                progress_bar.set(ratio)
                percent = int(ratio * 100)
                progress_label.configure(text=f"Saved ₹{saved} / ₹{target}  ({percent}%)")

                remaining = max(target - saved, 0)
                per_month = remaining / months
                suggestion_label.configure(
                    text=f"📆 Save ₹{per_month:.2f} per month to reach in {months} months.", text_color="#045B27")

                # Save to MongoDB
                dashboard_col.update_one(
    {"email": user_email},
    {
        "$set": {"funds": {
            "saved": saved,
            "target": target,
            "months": months
        }},
        "$push": {
            "history": {
                "amount": saved,
                "category": "Emergency Fund",
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        }
    },
    upsert=True
)

                   
                
                refresh_dashboard()
                

                # Show reset button if complete
                if saved == target:
                    reset_btn.pack(pady=10)
                else:
                    reset_btn.pack_forget()
            else:
                progress_label.configure(text="Enter valid amounts.", text_color="#D64545")
        except ValueError:
            progress_label.configure(text="Please enter valid numbers.", text_color="#D64545")
            suggestion_label.configure(text="")

    # === Update Button ===
    ctk.CTkButton(fund_win, text="Update Progress", font=text_font, fg_color="#06923E",
                  hover_color="#045B27", text_color="#FFFFFF", command=calculate_progress).pack(pady=15)


def open_currency_manager():
    win = ctk.CTkToplevel()
    win.title("Currency Manager")
    win.geometry("520x520")
    win.configure(fg_color="#D3ECCD")
    win.attributes('-topmost', True)

    # Fonts
    title_font = ctk.CTkFont(family="Gotham-Bold", size=30)
    text_font = ctk.CTkFont(family="Gotham-Bold", size=18)
    card_font = ctk.CTkFont(family="Gotham-Bold", size=20)

    ctk.CTkLabel(win, text="Currency Converter", font=title_font, text_color="#06923E").pack(pady=15)

    # === Amount Entry ===
    amount_entry = ctk.CTkEntry(
        win, placeholder_text="Enter amount",
        font=text_font, width=300,
        fg_color="white", text_color="#045B27", border_color="#06923E"
    )
    amount_entry.pack(pady=8)

    # === Currency Selection Frame ===
    currency_frame = ctk.CTkFrame(win, fg_color="#D3ECCD")
    currency_frame.pack(pady=5)

    from_currency = ctk.CTkComboBox(
        currency_frame, values=["INR", "USD", "EUR", "GBP"],
        font=text_font, width=120, dropdown_font=text_font,
        button_color="#06923E", button_hover_color="#045B27"
    )
    from_currency.set("INR")
    from_currency.pack(side="left", padx=5)

    swap_btn = ctk.CTkButton(
        currency_frame, text="🔁", width=50,
        font=ctk.CTkFont(family="Gotham-Bold", size=20),
        fg_color="#045B27", hover_color="#06923E",
        text_color="white", command=lambda: swap()
    )
    swap_btn.pack(side="left", padx=5)

    to_currency = ctk.CTkComboBox(
        currency_frame, values=["INR", "USD", "EUR", "GBP"],
        font=text_font, width=120, dropdown_font=text_font,
        button_color="#06923E", button_hover_color="#045B27"
    )
    to_currency.set("USD")
    to_currency.pack(side="left", padx=5)

    # === Result Label ===
    result_label = ctk.CTkLabel(win, text="", font=card_font, text_color="#045B27")
    result_label.pack(pady=15)

    # === Conversion History ===
    history_box = ctk.CTkTextbox(win, width=480, height=160,
                                 font=text_font, fg_color="#FFFFFF", text_color="#045B27", corner_radius=10)
    history_box.pack(pady=10)
    history_box.insert("0.0", "🧾 Conversion History:\n\n")
    history_box.configure(state="disabled")

    # === Exchange Rates ===
    conversion_rates = {
        "INR": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0098},
        "USD": {"INR": 83.5, "EUR": 0.92, "GBP": 0.82},
        "EUR": {"INR": 91.0, "USD": 1.09, "GBP": 0.89},
        "GBP": {"INR": 103.0, "USD": 1.21, "EUR": 1.12},
    }

    # === Swap Logic ===
    def swap():
        from_val = from_currency.get()
        to_val = to_currency.get()
        from_currency.set(to_val)
        to_currency.set(from_val)

    # === Conversion Logic ===
    def convert_currency():
        try:
            amt = float(amount_entry.get())
            from_cur = from_currency.get()
            to_cur = to_currency.get()

            if from_cur == to_cur:
                converted = amt
            else:
                converted = amt * conversion_rates[from_cur][to_cur]

            result_text = f"{amt:.2f} {from_cur} ≈ {converted:.2f} {to_cur}"
            result_label.configure(text=result_text, text_color="#045B27")

            # Add to history
            history_box.configure(state="normal")
            history_box.insert("end", f"{result_text}\n")
            history_box.configure(state="disabled")
        except:
            result_label.configure(text="❌ Enter valid numeric amount.", text_color="#D64545")

    # === Convert Button ===
    ctk.CTkButton(
        win, text="Convert", font=text_font,
        fg_color="#06923E", hover_color="#045B27",
        text_color="white", command=convert_currency
    ).pack(pady=10)

from datetime import datetime

def open_local_price_checker():
    win = ctk.CTkToplevel()
    win.geometry("520x620")
    win.title("Local Price Checker")
    win.configure(fg_color="#D3ECCD")
    win.attributes('-topmost', True)

    # Fonts
    title_font = ctk.CTkFont(family="Gotham-Bold", size=30)
    text_font = ctk.CTkFont(family="Gotham-Bold", size=18)
    card_font = ctk.CTkFont(family="Gotham-Bold", size=20)

    # MongoDB collection for price history
    price_history_col = db["price_checks"]

    # Title
    ctk.CTkLabel(win, text="🌍 Local Price Checker", font=title_font, text_color="#06923E").pack(pady=15)

    # Region Dropdown
    ctk.CTkLabel(win, text="Select Region", font=text_font, text_color="#045B27").pack(pady=5)
    region_combo = ctk.CTkComboBox(
        win, values=["India", "USA", "UK", "Germany", "Australia"],
        width=300, font=text_font, dropdown_font=text_font,
        button_color="#06923E", button_hover_color="#045B27"
    )
    region_combo.set("India")
    region_combo.pack(pady=5)

    # Product Dropdown
    ctk.CTkLabel(win, text="Select Product", font=text_font, text_color="#045B27").pack(pady=5)
    product_combo = ctk.CTkComboBox(
        win, values=["Milk", "Rice", "Bread", "Meal", "Oil", "Shampoo", "Taxi"],
        width=300, font=text_font, dropdown_font=text_font,
        button_color="#06923E", button_hover_color="#045B27"
    )
    product_combo.set("Milk")
    product_combo.pack(pady=5)

    # User Price Entry
    ctk.CTkLabel(win, text="Your Price (in ₹)", font=text_font, text_color="#045B27").pack(pady=5)
    price_entry = ctk.CTkEntry(
        win, width=300, placeholder_text="e.g. 55", font=text_font,
        fg_color="white", text_color="#045B27", border_color="#06923E"
    )
    price_entry.pack(pady=5)

    result_label = ctk.CTkLabel(win, text="", font=card_font, text_color="#045B27")
    result_label.pack(pady=15)

    # Local average price dataset
    averages = {
        "India": {"Milk": 55, "Rice": 45, "Bread": 40, "Meal": 150, "Oil": 130, "Shampoo": 180, "Taxi": 50},
        "USA": {"Milk": 92, "Rice": 115, "Bread": 120, "Meal": 1200, "Oil": 350, "Shampoo": 400, "Taxi": 250},
        "UK": {"Milk": 85, "Rice": 100, "Bread": 110, "Meal": 1000, "Oil": 340, "Shampoo": 360, "Taxi": 300},
        "Germany": {"Milk": 80, "Rice": 95, "Bread": 100, "Meal": 950, "Oil": 330, "Shampoo": 370, "Taxi": 280},
        "Australia": {"Milk": 88, "Rice": 105, "Bread": 115, "Meal": 1100, "Oil": 340, "Shampoo": 410, "Taxi": 270}
    }

    # === History Box ===
    history_label = ctk.CTkLabel(win, text="🧾 Recent Checks", font=card_font, text_color="#045B27")
    history_label.pack(pady=5)

    history_box = ctk.CTkTextbox(win, width=480, height=160,
                                 font=text_font, fg_color="#FFFFFF", text_color="#045B27", corner_radius=10)
    history_box.pack(pady=5)
    history_box.insert("0.0", "Fetching history...\n")
    history_box.configure(state="disabled")

    # Load history from MongoDB
    def load_history():
        history_box.configure(state="normal")
        history_box.delete("0.0", "end")

        recent_checks = price_history_col.find({"email": user_email}).sort("timestamp", -1).limit(5)
        found = False
        for record in recent_checks:
            found = True
            txt = f"{record['region']} - {record['product']}: ₹{record['price']} ({record['timestamp'].strftime('%d-%b %I:%M %p')})\n"
            history_box.insert("end", txt)
        if not found:
            history_box.insert("end", "No recent checks yet.\n")

        history_box.configure(state="disabled")

    # Initial load
    load_history()

    # === Check Price ===
    def check_price():
        region = region_combo.get()
        product = product_combo.get().strip().capitalize()
        try:
            user_price = float(price_entry.get())
            avg_price = averages.get(region, {}).get(product)

            if avg_price:
                diff = user_price - avg_price
                if abs(diff) <= 5:
                    msg = f"✅ Near Avg: ₹{avg_price}"
                    color = "#045B27"
                elif diff > 5:
                    msg = f"⚠️ High! You: ₹{user_price}, Avg: ₹{avg_price}"
                    color = "#D64545"
                else:
                    msg = f"💰 Good Deal! You: ₹{user_price}, Avg: ₹{avg_price}"
                    color = "#06923E"
            else:
                msg = "❌ Product not found in local data."
                color = "#D64545"

            result_label.configure(text=msg, text_color=color)

            # Log to MongoDB
            price_history_col.insert_one({
                "email": user_email,
                "region": region,
                "product": product,
                "price": user_price,
                "timestamp": datetime.now()
            })

            load_history()  # Reload history after save

        except ValueError:
            result_label.configure(text="❌ Enter a valid number.", text_color="#D64545")

    # Button
    ctk.CTkButton(
        win, text="Check Price", font=text_font,
        fg_color="#06923E", hover_color="#045B27",
        text_color="white", command=check_price
    ).pack(pady=10)




def open_medical_advisor():
    advisor_win = ctk.CTkToplevel()
    advisor_win.title("Medical Advisor")
    advisor_win.geometry("520x520")
    advisor_win.configure(fg_color="#D3ECCD")
    advisor_win.attributes("-topmost", True)

    # Fonts
    title_font = ctk.CTkFont(family="Gotham-Bold", size=30)
    text_font = ctk.CTkFont(family="Gotham-Bold", size=18)

    ctk.CTkLabel(advisor_win, text="🌍 Medical Advisor", font=title_font, text_color="#045B27").pack(pady=10)

    ctk.CTkLabel(advisor_win, text="Select Destination Country:", font=text_font, text_color="#045B27").pack(pady=5)

    countries = ["India", "USA", "UK", "Australia", "Germany", "Canada"]
    selected_country = ctk.StringVar(value="USA")

    country_dropdown = ctk.CTkOptionMenu(
        advisor_win,
        values=countries,
        variable=selected_country,
        width=300,
        font=text_font,
        dropdown_font=text_font,
        fg_color="#FFFFFF",
        text_color="#045B27",
        button_color="#06923E",
        button_hover_color="#045B27"
    )
    country_dropdown.pack(pady=10)

    output_box = ctk.CTkTextbox(
        advisor_win,
        width=460,
        height=320,
        font=text_font,
        corner_radius=10,
        text_color="#045B27",
        fg_color="#FFFFFF"
    )
    output_box.pack(pady=10, expand=True, fill="both", padx=10)

    default_advice = (
        "🧳 Basic Medical Tips (For All Travelers):\n"
        "- Always carry your prescription medicines.\n"
        "- Include paracetamol, ORS, band-aids, and sanitizer.\n"
        "- Check if vaccination is needed before travel.\n"
        "- Have digital & physical health insurance copies.\n"
        "- Emergency numbers vary by country — know them!\n"
        "\n🌐 Select a country to get specific advice."
    )
    output_box.insert("0.0", default_advice)

    country_data = {
        "USA": {
            "vaccines": "COVID-19, Influenza, MMR",
            "insurance": "Mandatory. Choose international/student plans.",
            "emergency": "911",
            "kit": "Painkillers, Band-Aids, Thermometer"
        },
        "UK": {
            "vaccines": "COVID-19, Meningitis, Hep B",
            "insurance": "Covered by NHS. Register with a GP.",
            "emergency": "999",
            "kit": "Antiseptic, Pain relief"
        },
        "Australia": {
            "vaccines": "COVID-19, Tetanus, Hep A",
            "insurance": "OSHC required for students.",
            "emergency": "000",
            "kit": "Sunscreen, Allergy meds"
        },
        "Germany": {
            "vaccines": "COVID-19, Polio, MMR",
            "insurance": "Public or private health insurance mandatory.",
            "emergency": "112",
            "kit": "Fever meds, Disinfectant"
        },
        "Canada": {
            "vaccines": "COVID-19, DTP, Hep B",
            "insurance": "Provincial or private insurance required.",
            "emergency": "911",
            "kit": "Cough syrup, First-aid kit"
        },
        "India": {
            "vaccines": "COVID-19, Typhoid, Hep A",
            "insurance": "Recommended. Buy travel/student plan.",
            "emergency": "112",
            "kit": "ORS, Mosquito repellent, Basic antibiotics"
        }
    }

    def show_advice():
        country = selected_country.get()
        info = country_data.get(country)

        if info:
            formatted = (
                f"🩺 Required Vaccines:\n- {info['vaccines']}\n\n"
                f"🏥 Health Insurance:\n- {info['insurance']}\n\n"
                f"🚨 Emergency Number:\n- {info['emergency']}\n\n"
                f"🧳 Recommended Travel Kit:\n- {info['kit']}\n"
            )
        else:
            formatted = "No specific advice available for this country."

        output_box.delete("0.0", "end")
        output_box.insert("0.0", formatted)
        output_box.configure(state="normal")
        output_box.delete("0.0", "end")
        output_box.insert("0.0", formatted)
        output_box.configure(state="disabled")


    ctk.CTkButton(
        advisor_win,
        text="Get Advice",
        font=text_font,
        fg_color="#06923E",
        hover_color="#045B27",
        text_color="#FFFFFF",
        command=show_advice
    ).pack(pady=10)

def open_bill_tracker():
    bill_win = ctk.CTkToplevel()
    bill_win.title("Bill & Subscription Tracker")
    bill_win.geometry("640x540")
    bill_win.configure(fg_color="#D3ECCD")
    bill_win.attributes('-topmost', True)

    # Fonts
    title_font = ctk.CTkFont(family="Gotham-Bold", size=30)
    text_font = ctk.CTkFont(family="Gotham-Bold", size=18)

    ctk.CTkLabel(bill_win, text="📅 Bill & Subscription Tracker", font=title_font, text_color="#06923E").pack(pady=15)

    name_entry = ctk.CTkEntry(bill_win, placeholder_text="Enter Bill Name (e.g., Netflix)", font=text_font, width=300)
    name_entry.pack(pady=5)

    amount_entry = ctk.CTkEntry(bill_win, placeholder_text="Enter Amount (₹)", font=text_font, width=300)
    amount_entry.pack(pady=5)

    due_date_entry = ctk.CTkEntry(bill_win, placeholder_text="Due Date (DD-MM-YYYY)", font=text_font, width=300)
    due_date_entry.pack(pady=5)

    result_frame = ctk.CTkFrame(bill_win, fg_color="white", width=540, height=270, corner_radius=8)
    result_frame.pack(pady=10)

    # === Load from DB
    user_data = dashboard_col.find_one({"email": user_email})
    bills = user_data.get("subscriptions", []) if user_data else []

    def update_list():
        for widget in result_frame.winfo_children():
            widget.destroy()

        today = date.today()
        sorted_bills = sorted(bills, key=lambda x: x["due"])

        for bill in sorted_bills:
            try:
                due_date = datetime.strptime(bill["due"], "%Y-%m-%d").date()
            except:
                continue

            name = bill["name"]
            amt = bill["amount"]
            days_left = (due_date - today).days

            if days_left < 0:
                status = f" Overdue by {-days_left} day(s)"
                color = "#D64545"
            elif days_left == 0:
                status = " !!!Due Today!!!"
                color = "#FFA500"
            else:
                status = f"Due in {days_left} day(s)"
                color = "#045B27"

            row = ctk.CTkFrame(result_frame, fg_color="white")
            row.pack(fill="x", padx=10, pady=3)

            label = ctk.CTkLabel(row, text=f"{name} - ₹{amt:.2f} | {due_date.strftime('%d-%b-%Y')} → {status}",
                                 font=text_font, text_color=color)
            label.pack(side="left", padx=5)

            del_btn = ctk.CTkButton(row, text="Delete", width=30, font=text_font,
                                    fg_color="#D64545", hover_color="#B22222",
                                    text_color="white",
                                    command=lambda b=bill: delete_bill(b))
            del_btn.pack(side="right")

    def add_bill():
        try:
            name = name_entry.get()
            amt = float(amount_entry.get())
            due_date_str = due_date_entry.get()
            due_date = datetime.strptime(due_date_str, "%d-%m-%Y").date()

            new_bill = {
                "name": name,
                "amount": amt,
                "due": due_date.strftime("%Y-%m-%d")
            }

            bills.append(new_bill)

            # ✅ Update subscriptions and PUSH to history for Category Breakdown
            dashboard_col.update_one(
                {"email": user_email},
                {
                    "$set": {"subscriptions": bills},
                    "$push": {
                        "history": {
                            "amount": amt,
                            "category": "Bills & Subscriptions",
                            "date": datetime.now().strftime("%Y-%m-%d")
                        }
                    }
                }
            )

            update_list()
            refresh_dashboard()  # ✅ Triggers pie chart update too

            days_left = (due_date - date.today()).days
            if days_left == 0:
                messagebox.showinfo("Reminder", f" '{name}' is Due Today!", parent=bill_win)
            elif 0 < days_left <= 3:
                messagebox.showinfo("Upcoming Bill", f" '{name}' due in {days_left} day(s).", parent=bill_win)

        except ValueError:
            messagebox.showerror("Invalid Input", "Enter valid amount & date (DD-MM-YYYY)", parent=bill_win)

    def delete_bill(bill):
        bills.remove(bill)
        dashboard_col.update_one(
            {"email": user_email},
            {"$set": {"subscriptions": bills}}
        )
        update_list()
        refresh_dashboard()

    def export_csv():
        if not bills:
            messagebox.showwarning("Empty", "No bills to export.", parent=bill_win)
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Bill Data",
            initialfile="bills_export.csv",
            parent=bill_win
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Bill Name", "Amount (₹)", "Due Date"])
                for bill in bills:
                    writer.writerow([bill["name"], bill["amount"], bill["due"]])

            messagebox.showinfo("Exported", f"✅ Bills exported to:\n{file_path}", parent=bill_win)
        except Exception as e:
            messagebox.showerror("Export Error", str(e), parent=bill_win)

    # Buttons
    add_btn = ctk.CTkButton(bill_win, text="Add Bill", font=text_font, fg_color="#06923E",
                            hover_color="#045B27", command=add_bill)
    add_btn.pack(pady=5)

    export_btn = ctk.CTkButton(bill_win, text="Export CSV", font=text_font, fg_color="#FFA500",
                               hover_color="#CC8400", command=export_csv)
    export_btn.pack(pady=5)

    update_list()


def open_ai_financial_advisor():
    chat_win = ctk.CTkToplevel()
    chat_win.title("AI Financial Advisor")
    chat_win.geometry("520x550")
    chat_win.configure(fg_color="#D3ECCD")
    chat_win.attributes("-topmost", True)

    # Fonts
    title_font = ctk.CTkFont(family="Gotham-Bold", size=30)
    text_font = ctk.CTkFont(family="Gotham-Bold", size=18)

    ctk.CTkLabel(chat_win, text="Ask your Financial Advisor 🤖", font=title_font, text_color="#06923E").pack(pady=10)

    # Chat Display Box
    chat_box = ctk.CTkTextbox(
        chat_win,
        width=480,
        height=380,
        font=text_font,
        fg_color="#FFFFFF",
        text_color="#045B27",
        corner_radius=8
    )
    chat_box.pack(pady=10)
    chat_box.insert("0.0", " Hi! I'm your SmartFinance AI.\nAsk me anything about savings, budgeting, or financial goals.\n\n")

    # User Entry Field
    user_entry = ctk.CTkEntry(chat_win, width=400, placeholder_text="Type your question here...", font=text_font)
    user_entry.pack(pady=5)

    def send_to_ai():
        user_question = user_entry.get()
        if not user_question.strip():
            return

        chat_box.insert("end", f" You: {user_question}\n")
        chat_box.insert("end", " SmartFinance is typing...\n")
        chat_box.see("end")


        # === OpenRouter API Call ===
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful financial advisor. Keep answers short, practical, and friendly."},
                {"role": "user", "content": user_question}
            ]
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"]
                chat_box.insert("end", f" SmartFinance: {reply.strip()}\n\n")
            else:
                chat_box.insert("end", f" Error: {response.status_code} - Could not get response.\n\n")

        except Exception as e:
            chat_box.insert("end", f" Exception: {e}\n\n")

        # Clear input
        user_entry.delete(0, "end")

    ctk.CTkButton(
        chat_win,
        text="Ask",
        font=text_font,
        fg_color="#06923E",
        hover_color="#045B27",
        text_color="white",
        command=send_to_ai
    ).pack(pady=10)

def open_goal_tracker():
    print("✅ Goal Tracker triggered")

    # Prevent multiple windows
    if hasattr(open_goal_tracker, "is_open") and open_goal_tracker.is_open:
        return
    open_goal_tracker.is_open = True

    # Create modal window
    goal_win = ctk.CTkToplevel(master=root)
    goal_win.title("Goal Tracker")
    goal_win.geometry("600x600")
    goal_win.configure(fg_color="#D3ECCD")

    # Proper modal behavior
    goal_win.withdraw()
    goal_win.update_idletasks()
    goal_win.deiconify()
    goal_win.grab_set()           # Make it modal
    goal_win.lift()               # Bring it front
    goal_win.focus_force()
    goal_win.attributes('-topmost', True)
    goal_win.after(10, lambda: goal_win.attributes('-topmost', False))


    def on_close():
        open_goal_tracker.is_open = False
        goal_win.grab_release()
        goal_win.destroy()

    goal_win.protocol("WM_DELETE_WINDOW", on_close)

    # Fonts
    title_font = ctk.CTkFont(family="Gotham-Bold", size=30)
    text_font = ctk.CTkFont(family="Gotham-Bold", size=18)

    # UI Elements
    ctk.CTkLabel(goal_win, text="🎯 Goal Tracker", font=title_font, text_color="#06923E").pack(pady=15)
    name_entry = ctk.CTkEntry(goal_win, placeholder_text="Enter Goal Name", font=text_font, width=300)
    target_entry = ctk.CTkEntry(goal_win, placeholder_text="Target Amount (₹)", font=text_font, width=300)
    saved_entry = ctk.CTkEntry(goal_win, placeholder_text="Saved Amount (₹)", font=text_font, width=300)
    for entry in (name_entry, target_entry, saved_entry): entry.pack(pady=5)

    goal_list_frame = ctk.CTkScrollableFrame(goal_win, width=550, height=350, fg_color="#FFFFFF")
    goal_list_frame.pack(pady=10)

    user_data = dashboard_col.find_one({"email": user_email})
    goals = user_data.get("goals", []) if user_data else []

    def get_progress_color(ratio):
        return "#06923E" if ratio >= 0.75 else "#F6BE00" if ratio >= 0.4 else "#D64545"

    def update_goals():
        for widget in goal_list_frame.winfo_children():
            widget.destroy()

        for i, goal in enumerate(goals):
            goal_name = goal["name"]
            target = goal["target"]
            saved = goal["saved"]
            progress = min(saved / target, 1.0) if target > 0 else 0
            percent = int(progress * 100)

            label = ctk.CTkLabel(goal_list_frame,
                text=f"🔸 {goal_name}: ₹{saved:.2f} / ₹{target:.2f} ({percent}%)",
                font=text_font, text_color="#045B27", anchor="w", justify="left", wraplength=500)
            label.grid(row=i*2, column=0, columnspan=3, sticky="w", padx=10, pady=5)

            progress_bar = ctk.CTkProgressBar(goal_list_frame, width=400, height=12,
                                              progress_color=get_progress_color(progress))
            progress_bar.set(progress)
            progress_bar.grid(row=i*2+1, column=0, padx=10, sticky="w")

            # Edit Button
            def edit_goal(index=i):
                new_saved = simpledialog.askfloat("Update Saved Amount",
                    f"Enter updated saved amount for '{goals[index]['name']}':", parent=goal_win)
                if new_saved is not None and new_saved >= 0:
                    goals[index]["saved"] = new_saved
                    dashboard_col.update_one({"email": user_email}, {"$set": {"goals": goals}})
                    update_goals()
                    refresh_dashboard()

            edit_btn = ctk.CTkButton(goal_list_frame, text="Edit", width=40, height=24, font=text_font,
                                     command=edit_goal, fg_color="#F6BE00", text_color="white",
                                     hover_color="#D9A300")
            edit_btn.grid(row=i*2+1, column=1, padx=2, sticky="e")

            # Delete Button
            def delete_goal(index=i):
                goal_name = goals[index]["name"]
                confirm = messagebox.askyesno("Delete Goal", f"Delete goal '{goal_name}'?", parent=goal_win)
                if confirm:
                    del goals[index]
                    dashboard_col.update_one({"email": user_email}, {"$set": {"goals": goals}})
                    update_goals()
                    refresh_dashboard()

            delete_btn = ctk.CTkButton(goal_list_frame, text="Delete", width=40, height=24, font=text_font,
                                       command=delete_goal, fg_color="#D64545", text_color="white",
                                       hover_color="#B33333")
            delete_btn.grid(row=i*2+1, column=2, padx=2)

    def add_goal():
        try:
            name = name_entry.get().strip()
            target = float(target_entry.get())
            saved = float(saved_entry.get())

            if not name or target <= 0 or saved < 0:
                raise ValueError

            progress = min(saved / target, 1.0)
            goals.append({"name": name, "target": target, "saved": saved, "progress": progress})
            dashboard_col.update_one({"email": user_email}, {"$set": {"goals": goals}})
            update_goals()

            # Clear inputs
            for entry in (name_entry, target_entry, saved_entry):
                entry.delete(0, "end")

        except ValueError:
            messagebox.showerror("Invalid Input", "❌ Please enter valid numeric values.", parent=goal_win)

    ctk.CTkButton(goal_win, text="Add Goal", font=text_font, command=add_goal,
                  fg_color="#06923E", hover_color="#045B27", text_color="#FFFFFF").pack(pady=10)

    update_goals()
    


# === Sidebar Features ===
features = {
    "Emergency Fund Tracker": open_emergency_fund,
    "Currency Manager": open_currency_manager,
    "Local Price Checker": open_local_price_checker,
    "Medical Advisor": open_medical_advisor,
    "AI Financial Advisor": open_ai_financial_advisor,
    "Bill & Subscription Tracker": open_bill_tracker,
    "Goal-Based Savings Tracker": open_goal_tracker,
}

for label, func in features.items():
    ctk.CTkButton(
        sidebar,
        text=label,
        font=text_font,
        corner_radius=10,
        fg_color="#06923E",          # Primary Green
        hover_color="#045B27",       # Darker hover green
        text_color="#FFFFFF",        # White text
        command=func
    ).pack(pady=8, padx=10, fill="x")

# === Logout Button ===
ctk.CTkButton(
    sidebar,
    text="Logout",
    font=text_font,
    fg_color="#D64545",             # Red logout
    hover_color="#B33333",
    text_color="#FFFFFF",
    command=root.destroy
).pack(side="bottom", pady=20, padx=10)

# # === Header Cards ===
# header = ctk.CTkFrame(root, fg_color="#D3ECCD")  # Light green header background
# header.pack(fill="x", padx=30, pady=10)


# # === Header Card Creator ===
# def create_card(parent, title, amount, color):
#     card = ctk.CTkFrame(parent, fg_color=color, width=250, height=80, corner_radius=10)
#     card.pack(side="left", padx=15)
#     ctk.CTkLabel(card, text=title, font=card_font, text_color="white").pack(anchor="w", padx=10, pady=5)
#     label = ctk.CTkLabel(card, text=f"₹ {amount}", font=card_font, text_color="white")
#     label.pack(anchor="w", padx=10)
#     return label  # ✅ Return for updating later

# === Header Card Widgets (only once) ===
# total_balance_label = create_card(header, "Total Balance", "0", "#045B27")       # Dark green
# monthly_expense_label = create_card(header, "Monthly Expenses", "0", "#D64545")  # Red
# savings_label = create_card(header, "Savings", "0", "#06923E")                   # Primary green

# # === Graph Section (Dynamic) ===
# chart_area = ctk.CTkFrame(root, fg_color="#D3ECCD")
# chart_area.pack(fill="both", expand=True, padx=20, pady=10)

# Line Graph - Financial Growth
fig1 = Figure(figsize=(5, 3), dpi=100)
ax1 = fig1.add_subplot(111)
canvas1 = FigureCanvasTkAgg(fig1, master=chart_area)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left", padx=20)

# Pie Charts (Spending + Category Breakdown)
fig2 = Figure(figsize=(5, 3), dpi=100)
ax2 = fig2.add_subplot(121)
ax3 = fig2.add_subplot(122)
canvas2 = FigureCanvasTkAgg(fig2, master=chart_area)
canvas2.draw()
canvas2.get_tk_widget().pack(side="right", padx=20)

# === Initial Load & Live Updates ===
refresh_dashboard()
auto_refresh()


root.mainloop()