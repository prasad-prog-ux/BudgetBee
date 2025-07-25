import tkinter as tk
from tkinter import ttk
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure



root = tk.Tk()
root.title("SmartFinance Dashboard")
root.geometry("1080x720")
root.configure(bg="#D3ECCD")

# Fonts
title_font = ("Inter", 22, "bold")
subtitle_font = ("Inter", 16)
card_font = ("Inter", 14)

# ==== Header ====
header = tk.Frame(root, bg="#D3ECCD")
header.pack(fill="x", padx=20, pady=10)

tk.Label(header, text="SmartFinance", font=title_font, fg="#06923E", bg="#D3ECCD").pack(side="left")
tk.Button(header, text="Logout", font=subtitle_font, bg="#06923E", fg="white", padx=10).pack(side="right", padx=10)

# ==== Summary Cards ====
cards_frame = tk.Frame(root, bg="#D3ECCD")
cards_frame.pack(pady=10)

def create_card(master, title, amount, bg_color):
    card = tk.Frame(master, bg=bg_color, width=250, height=100)
    card.pack(side="left", padx=20)
    tk.Label(card, text=title, font=subtitle_font, bg=bg_color, fg="white").pack(anchor="w", padx=10, pady=5)
    tk.Label(card, text=f"₹ {amount}", font=("Inter", 18, "bold"), bg=bg_color, fg="white").pack(anchor="w", padx=10)

create_card(cards_frame, "💰 Total Balance", "12,500", "#3E8E41")  # Green
create_card(cards_frame, "📉 Monthly Expenses", "5,300", "#D64545")  # Red
create_card(cards_frame, "📈 Savings", "7,200", "#06923E")  # Dark green

# ==== Charts ====
chart_frame = tk.Frame(root, bg="#D3ECCD")
chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Pie chart
fig1 = Figure(figsize=(3.5, 3), dpi=100)
ax1 = fig1.add_subplot(111)
ax1.pie([5300, 7200], labels=["Expenses", "Savings"], colors=["#D64545", "#06923E"], autopct='%1.1f%%')
ax1.set_title("Spending Distribution")

canvas1 = FigureCanvasTkAgg(fig1, master=chart_frame)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left", padx=10)

# Bar chart
fig2 = Figure(figsize=(4.5, 3), dpi=100)
ax2 = fig2.add_subplot(111)
months = ["Jan", "Feb", "Mar", "Apr", "May"]
expenses = [4000, 4500, 5000, 5300, 4900]
savings = [6000, 5800, 6200, 7000, 7200]

ax2.bar(months, expenses, label="Expenses", color="#D64545")
ax2.bar(months, savings, label="Savings", color="#06923E", bottom=expenses)
ax2.set_title("Monthly Finance Trend")
ax2.legend()

canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame)
canvas2.draw()
canvas2.get_tk_widget().pack(side="right", padx=10)

# ==== Scrollable Feature Cards ====
scroll_frame = tk.Frame(root, bg="#D3ECCD")
scroll_frame.pack(fill="both", padx=20, pady=10, expand=True)

canvas = tk.Canvas(scroll_frame, bg="#D3ECCD", highlightthickness=0)
scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#D3ECCD")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Sample features
features = [
    ("📊 Emergency Fund Tracker", "Ensure your future with smart reserves."),
    ("💳 Multi-Currency Manager", "Real-time exchange and alerts."),
    ("📌 Local Price Checker", "Compare local prices and get smart ranges."),
    ("🗓️ Semester Budget Planner", "Plan for books, food, and transport."),
    ("🚨 Visa Expense Alerts", "Track visa-related expenses on the go.")
]

for title, desc in features:
    feature_card = tk.Frame(scrollable_frame, bg="white", bd=1, relief="solid")
    feature_card.pack(pady=10, fill="x", padx=10)
    tk.Label(feature_card, text=title, font=subtitle_font, bg="white", fg="#06923E").pack(anchor="w", padx=10, pady=5)
    tk.Label(feature_card, text=desc, font=card_font, bg="white", fg="black", wraplength=800, justify="left").pack(anchor="w", padx=10)

root.mainloop()
