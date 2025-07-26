import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import requests
import subprocess
import sys
# === API Keys ===
OPENROUTER_API_KEY = "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"
NEWS_API_KEY = "cdf42d910fc7411c8b80b187c4fc0431"


# === App Setup ===
app = ctk.CTk()
app.title("SmartFinance Landing Page")
app.geometry("1280x720")
# app.resizable(False, False)

bg = ctk.CTkFrame(app, fg_color="#D3ECCD")
bg.pack(fill="both", expand=True)

# === Theme & Fonts ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

font_heading = ctk.CTkFont("Gotham-Bold", 36)
font_button = ctk.CTkFont("Gotham-Bold", 18)
font_text = ctk.CTkFont("Gotham-Bold", 14)
title_font = ctk.CTkFont("Gotham-Bold", 28)
card_font = ctk.CTkFont("Gotham-Bold", 16)
def open_login():
    subprocess.Popen([sys.executable, "loginnew.py"],)
    app.after(500, app.destroy)  # Delay closing after 0.5 sec

# === About Us Window ===
def open_about():
    win = ctk.CTkToplevel(fg_color="#D3ECCD")
    win.title("About Us")
    win.geometry("500x300")
    win.attributes("-topmost", True)

    about_text = (
        "SmartFinance is your personal finance assistant designed to help you track expenses, "
        "manage savings, convert currencies, and stay updated with the latest financial news."
    )
    ctk.CTkLabel(win, text="About SmartFinance", font=title_font, text_color="#045B27").pack(pady=10)
    tb = ctk.CTkTextbox(win, height=180, width=460, font=font_text,
                        fg_color="white", text_color="#045B27")
    tb.pack(pady=10)
    tb.insert("0.0", about_text)
    tb.configure(state="disabled")

# === Contact Us Window ===
def open_contact():
    win = ctk.CTkToplevel(fg_color="#D3ECCD")
    win.title("Contact Us")
    win.geometry("500x400")
    win.attributes('-topmost', True)

    ctk.CTkLabel(win, text="Contact Us", font=title_font, text_color="#045B27").pack(pady=15)
    ctk.CTkEntry(win, placeholder_text="Your Name", font=font_text, width=350,
                 fg_color="white", text_color="#045B27").pack(pady=10)
    ctk.CTkEntry(win, placeholder_text="Your Email", font=font_text, width=350,
                 fg_color="white", text_color="#045B27").pack(pady=10)
    ctk.CTkTextbox(win, height=120, width=350, font=font_text,
                   fg_color="white", text_color="#045B27").pack(pady=10)
    ctk.CTkButton(win, text="Send", font=font_text, fg_color="#06923E",
                  hover_color="#045B27", text_color="white").pack(pady=10)

# === Currency Converter Window ===
def open_currency_manager():
    win = ctk.CTkToplevel(fg_color="#D3ECCD")
    win.title("Currency Manager")
    win.geometry("500x450")
    win.attributes('-topmost', True)

    ctk.CTkLabel(win, text="Currency Converter", font=title_font, text_color="#045B27").pack(pady=20)

    amount_entry = ctk.CTkEntry(win, placeholder_text="Enter amount", font=font_text,
                                fg_color="white", text_color="#045B27", width=300, border_color="#06923E")
    amount_entry.pack(pady=10)

    from_currency = ctk.CTkComboBox(win, values=["INR", "USD", "EUR", "GBP"], font=font_text,
                                    width=140, dropdown_font=font_text)
    from_currency.set("INR")
    from_currency.pack(pady=5)

    to_currency = ctk.CTkComboBox(win, values=["INR", "USD", "EUR", "GBP"], font=font_text,
                                  width=140, dropdown_font=font_text)
    to_currency.set("USD")
    to_currency.pack(pady=5)

    result_label = ctk.CTkLabel(win, text="", font=card_font, text_color="#045B27")
    result_label.pack(pady=15)

    conversion_rates = {
        "INR": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0098},
        "USD": {"INR": 83.5, "EUR": 0.92, "GBP": 0.82},
        "EUR": {"INR": 91.0, "USD": 1.09, "GBP": 0.89},
        "GBP": {"INR": 103.0, "USD": 1.21, "EUR": 1.12},
    }

    def convert_currency():
        try:
            amt = float(amount_entry.get())
            from_cur = from_currency.get()
            to_cur = to_currency.get()
            converted = amt if from_cur == to_cur else amt * conversion_rates[from_cur][to_cur]
            result_label.configure(text=f"{amt:.2f} {from_cur} ≈ {converted:.2f} {to_cur}")
        except Exception:
            result_label.configure(text="Enter valid numbers.")

    ctk.CTkButton(win, text="Convert", font=font_text, fg_color="#06923E",
                  hover_color="#045B27", command=convert_currency).pack(pady=10)

# === AI Advisor ===
def ask_deepseek_chat(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "SmartFinance"
        }
        payload = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful financial advisor."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = res.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"❌ API Error: {data['error'].get('message', 'Unknown error')}"
        return "❌ Unexpected response format."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def open_ai_advisor():
    win = ctk.CTkToplevel(fg_color="#D3ECCD")
    win.title("AI Advisor")
    win.geometry("520x580")
    win.attributes("-topmost", True)

    ctk.CTkLabel(win, text="Ask your Financial Advisor 🤖", font=title_font, text_color="#045B27").pack(pady=10)
    chat_box = ctk.CTkTextbox(win, width=480, height=380, font=font_text,
                              fg_color="white", text_color="#045B27")
    chat_box.pack(pady=10)
    chat_box.insert("0.0", "👋 Hi! I'm your SmartFinance Advisor.\nAsk anything about savings, budgeting, or finance.\n\n")

    user_entry = ctk.CTkEntry(win, width=400, placeholder_text="Type your question here...", font=font_text)
    user_entry.pack(pady=5)

    def on_ask():
        q = user_entry.get().strip()
        if not q: return
        chat_box.insert("end", f"You: {q}\n🤖 Advisor: Thinking...\n\n")
        user_entry.delete(0, "end")
        def update():
            reply = ask_deepseek_chat(q)
            chat_box.delete("end-3l", "end-1l")
            chat_box.insert("end", f"🤖 Advisor: {reply}\n\n")
        app.after(100, update)

    ctk.CTkButton(win, text="Ask", font=font_text, width=80, fg_color="#06923E",
                  hover_color="#045B27", command=on_ask).pack(pady=5)

# === News ===
def open_latest_news():
    win = ctk.CTkToplevel(fg_color="#D3ECCD")
    win.title("Latest News")
    win.geometry("600x500")
    win.attributes('-topmost', True)

    ctk.CTkLabel(win, text="Finance Headlines", font=title_font, text_color="#045B27").pack(pady=10)
    global news_box
    news_box = ctk.CTkTextbox(win, width=560, height=400, font=font_text,
                              fg_color="white", text_color="#045B27")
    news_box.pack(pady=10)
    fetch_news()

def fetch_news():
    news_box.configure(state="normal")
    news_box.delete("0.0", "end")
    try:
        url = f"https://newsapi.org/v2/everything?q=finance&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
        r = requests.get(url)
        data = r.json()
        if data.get("status") == "ok":
            for i, article in enumerate(data["articles"], 1):
                title = article.get("title", "No Title")
                source = article.get("source", {}).get("name", "Unknown")
                link = article.get("url", "")
                news_box.insert("end", f"{i}. {title}\nSource: {source}\n{link}\n\n")
        else:
            raise Exception("No news returned.")
    except Exception as e:
        news_box.insert("0.0", f"❌ Failed to load news:\n{e}")
    finally:
        news_box.configure(state="disabled")

# === Navbar ===
navbar = ctk.CTkFrame(bg, height=60, fg_color="#B2FFDA")  # Light greenish background

navbar.pack(fill="x", side="top")
ctk.CTkLabel(navbar, text="SmartFinance", font=font_heading, text_color="#045B27").pack(side="left", padx=30)



nav_btns = ctk.CTkFrame(navbar, fg_color="transparent")
nav_btns.pack(side="right", padx=30)

ctk.CTkButton(nav_btns, text="About Us", font=font_button, command=open_about,
              fg_color="#045B27", hover_color="#06923E", text_color="white").pack(side="left", padx=10)
ctk.CTkButton(nav_btns, text="Contact", font=font_button, command=open_contact,
              fg_color="#045B27", hover_color="#06923E", text_color="white").pack(side="left", padx=10)

# === Hero Section ===
main_frame = ctk.CTkFrame(bg, fg_color="transparent")
main_frame.pack(pady=80)
ctk.CTkLabel(main_frame, text="Smarter Finance. Better Life.", font=font_heading, text_color="#045B27").pack(pady=10)
ctk.CTkLabel(main_frame, text="Manage emergency funds, currency, AI queries, and news — all in one place.",
             font=font_text, text_color="#045B27").pack(pady=10)
ctk.CTkButton(main_frame, text="Get Started", font=font_button, width=200, height=50,
              fg_color="#06923E", hover_color="#045B27", command=open_login).pack(pady=20)


# === Features ===
feature_frame = ctk.CTkFrame(bg, fg_color="transparent")
feature_frame.pack(pady=30)

def feature_card(title, desc, func):
    card = ctk.CTkFrame(feature_frame, fg_color="#FFFFFF", width=300, height=220, corner_radius=10)
    card.pack_propagate(False)
    card.pack(side="left", padx=20)
    ctk.CTkLabel(card, text=title, font=font_button, text_color="#045B27").pack(pady=10)
    ctk.CTkLabel(card, text=desc, font=font_text, text_color="#06923E", wraplength=260, justify="center").pack()
    ctk.CTkButton(card, text="Try Now", font=font_text, width=120, height=28,
                  fg_color="#06923E", hover_color="#045B27", command=func, text_color="white").pack(pady=10)

feature_card("AI Advisor", "Ask anything about saving, goals, or budgeting.", open_ai_advisor)
feature_card("Currency Converter", "Convert INR, USD, EUR, GBP instantly.", open_currency_manager)
feature_card("📢 Latest News", "Get the latest finance and economy headlines.", open_latest_news)

# === Start App ===
app.mainloop()
