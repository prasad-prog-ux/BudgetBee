import tkinter as tk
from tkinter import ttk
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Main Window
root = tk.Tk()
root.title("SmartFinance Dashboard")
root.geometry("1200x700")
root.config(bg="#0F0F0F")

# Fonts
title_font = font.Font(family="Helvetica", size=24, weight="bold")
card_font = font.Font(family="Helvetica", size=14, weight="bold")
text_font = font.Font(family="Helvetica", size=12)

# Header
header = tk.Frame(root, bg="#0F0F0F")
header.pack(fill='x', pady=10)

tk.Label(header, text="SmartFinance", font=title_font, fg="#FFD700", bg="#0F0F0F").pack(side="left", padx=20)
tk.Button(header, text="Settings", font=text_font, bg="#FFD700", fg="black", bd=0, padx=15).pack(side="right", padx=20)

# Main Content Frame
main = tk.Frame(root, bg="#0F0F0F")
main.pack(fill="both", expand=True, padx=20)

# ===== Left Side: Cards + Pie Chart =====
left_frame = tk.Frame(main, bg="#0F0F0F")
left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Feature Cards
def create_card(parent, title, value, color):
    frame = tk.Frame(parent, bg=color, width=300, height=100)
    frame.pack_propagate(False)
    frame.pack(pady=10, fill="x")

    tk.Label(frame, text=title, font=card_font, bg=color, fg="black").pack(anchor="w", padx=10, pady=(10, 0))
    tk.Label(frame, text=value, font=text_font, bg=color, fg="black").pack(anchor="w", padx=10)

create_card(left_frame, "💰 Total Balance", "₹75,000", "#FFD700")
create_card(left_frame, "⚠️ Emergency Fund", "₹15,000", "#FFA500")
create_card(left_frame, "📅 Monthly Budget", "₹30,000", "#ADFF2F")

# Pie Chart (Matplotlib)
fig, ax = plt.subplots(figsize=(3.5, 3.5), dpi=100)
categories = ['Essentials', 'Savings', 'Entertainment', 'Other']
amounts = [40, 25, 20, 15]
colors = ['#FFD700', '#FFA500', '#ADFF2F', '#C0C0C0']
ax.pie(amounts, labels=categories, colors=colors, autopct='%1.1f%%')
ax.set_title("Spending Breakdown", color="white")
fig.patch.set_facecolor('#0F0F0F')

canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.draw()
canvas.get_tk_widget().pack(pady=20)

# ===== Right Side: Scrollable Transactions =====
right_frame = tk.Frame(main, bg="#0F0F0F")
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tk.Label(right_frame, text="💸 Recent Transactions", font=card_font, bg="#0F0F0F", fg="#FFD700").pack(anchor="w")

# Scrollable Frame
canvas = tk.Canvas(right_frame, bg="#1A1A1A", bd=0, highlightthickness=0, height=400)
scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1A1A1A")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Dummy transactions
transactions = [
    ("Dominos Pizza", "-₹500"),
    ("Metro Card Recharge", "-₹100"),
    ("Library Fine", "-₹50"),
    ("Part-time Salary", "+₹6,000"),
    ("Amazon Order", "-₹1,200"),
    ("Café Coffee Day", "-₹220"),
]

for name, amt in transactions:
    frame = tk.Frame(scrollable_frame, bg="#262626", pady=10)
    tk.Label(frame, text=name, font=text_font, bg="#262626", fg="white").pack(side="left", padx=10)
    tk.Label(frame, text=amt, font=text_font, bg="#262626", fg="lightgreen" if "+" in amt else "#FF6961").pack(side="right", padx=10)
    frame.pack(fill="x", padx=10, pady=5)

# Run the app
root.mainloop()
