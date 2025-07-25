from tkinter import *
import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
from pymongo import MongoClient

import os

# === MongoDB Connection ===
client = MongoClient("mongodb://localhost:27017/")
db = client["smartfinance"]
users_col = db["users"]

# === Appearance ===
ctk.set_appearance_mode("dark")

# === Window Setup ===
login = ctk.CTk()
login.title("SmartFinance Login")
login.geometry("1080x720")
login.resizable(False, False)

# === Fonts ===
my_font_heading = ctk.CTkFont(family="Gotham-Bold", size=42)
my_font_subheading = ctk.CTkFont(family="Gotham-Bold", size=30)
my_font_label1 = ctk.CTkFont(family="Gotham-Bold", size=28)
my_font_label2 = ctk.CTkFont(family="Gotham-Bold", size=18)
my_font_button = ctk.CTkFont(family="Gotham-Bold", size=20, underline=True)

# === Layout ===
main_frame = ctk.CTkFrame(master=login, width=1080, height=720, fg_color="#D3ECCD")
main_frame.place(x=0, y=0)

logo = ctk.CTkLabel(main_frame, text="SmartFinance ", font=my_font_heading, text_color="#06923E")
logo.place(x=50, y=240)

descrp = ctk.CTkLabel(main_frame, text="Manage your money, smartly.", font=my_font_subheading, text_color="#06923E")
descrp.place(x=50, y=310)

shadow = ctk.CTkFrame(main_frame, width=410, height=410, corner_radius=25, fg_color="#b8dbb8")
shadow.place(x=604, y=154)

login_box = ctk.CTkFrame(main_frame, width=400, height=400, corner_radius=25,
                         fg_color="#ffffff", bg_color="#ffffff",
                         border_color="#06923E", border_width=1)
login_box.place(x=600, y=150)

header_strip = ctk.CTkFrame(login_box, width=400, height=5, fg_color="#06923E")
header_strip.place(x=0, y=0)

title = ctk.CTkLabel(login_box, text="Sign In", font=my_font_label1, text_color="#06923E")
title.place(x=20, y=20)

# === Login Fields ===
entry_email = ctk.CTkEntry(login_box, font=my_font_label2, placeholder_text="📧 Email", width=350, height=40,
                            fg_color="white", border_color="#06923E", corner_radius=10)
entry_email.place(x=20, y=80)

entry_password = ctk.CTkEntry(login_box, font=my_font_label2, placeholder_text="🔒 Password", width=350, height=40,
                               fg_color="white", border_color="#06923E", corner_radius=10, show="*")
entry_password.place(x=20, y=135)

info = ctk.CTkLabel(login_box, text="Minimum 6 characters", font=my_font_label2, text_color="gray")
info.place(x=20, y=175)

# === Login Logic ===

def login_user():
    email = entry_email.get().strip()
    password = entry_password.get().strip()

    if not email or not password:
        messagebox.showerror("Error", "Please enter both email and password.")
        return

    user = users_col.find_one({"email": email, "password": password})
    if user:
        messagebox.showinfo("Success", f"Welcome back, {user['name']}!")
        login.destroy()

        # ✅ Open dashboard.py properly using sys.executable and without CMD window
        subprocess.Popen(
            [sys.executable, os.path.abspath("dashboard.py"), email],
              # 👈 hides CMD window
        )
    else:
        messagebox.showerror("Login Failed", "Invalid email or password.")


# === Login Button ===
login_btn = ctk.CTkButton(login_box, text="🔓 Login Now", font=my_font_label2, height=40, width=350,
                           text_color="#D3ECCD", fg_color="#06923E", hover_color="#045B27",
                           command=login_user)
login_btn.place(x=20, y=215)

# === Signup Redirect ===
or_line = ctk.CTkFrame(login_box, width=350, height=1, fg_color="#b0b0b0")
or_line.place(x=20, y=270)

switch_label = ctk.CTkLabel(login_box, text="Don't have an account?", font=my_font_label2, text_color="#06923E")
switch_label.place(x=20, y=290)

def open_signup():
    login.destroy()
    subprocess.Popen([sys.executable, "signup.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)

signup_btn = ctk.CTkButton(login_box, text="Sign Up →", font=my_font_button, height=30, width=120,
                            text_color="#06923E", fg_color="white", hover_color="#eeeeee", command=open_signup)
signup_btn.place(x=230, y=285)

# === Focus Handling ===
login.lift()
login.attributes("-topmost", True)
login.after(500, lambda: login.attributes("-topmost", False))

login.mainloop()
