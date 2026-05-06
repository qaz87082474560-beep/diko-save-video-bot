import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8654475059:AAHjZD5cZAe-JWcTZzKzjQvutEq4yNOYGTg"
ADMIN_ID = 6617415280

bot = telebot.TeleBot(TOKEN)

users = set()

# MENU
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    KeyboardButton("📄 ЭЦП"),
    KeyboardButton("🆔 IMEI")
)
menu.add(
    KeyboardButton("🛂 Паспорт"),
    KeyboardButton("✈️ K-ETA")
)
menu.add(
    KeyboardButton("💼 Чет элда иш"),
    KeyboardButton("❓ Савол бериш")
)

# START
@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)
    bot.send_message(
        message.chat.id,
        "👋 Tez Hujjat botiga xush kelibsiz 🇰🇿",
        reply_markup=menu
    )

# ADMIN
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "👑 Admin panel ishlayapti")
    else:
        bot.send_message(message.chat.id, "⛔ Siz admin emassiz")

# SMART AI (FREE)
def smart_ai(text):
    text = text.lower()

    # keyword AI
    if "эцп" in text:
        return "📄 ЭЦП: pki.gov.kz orqali olinadi, NCALayer o‘rnatiladi."

    if "imei" in text:
        return "🆔 IMEI: imei.rfs.gov.kz saytidan tekshiriladi."

    if "паспорт" in text:
        return "🛂 Паспорт: egov.kz orqali tekshiriladi."

    if "корея" in text or "k-eta" in text:
        return "✈️ K-ETA: Koreyaga kirish uchun online ariza to‘ldiriladi."

    if "иш" in text:
        return "💼 Ish: faqat rasmiy agentliklardan foydalaning."

    if "салом" in text or "salom" in text:
        return "👋 Salom! Sizga qanday yordam bera olaman?"

    # default AI answer
    return (
        "🤖 Men sizni tushundim.\n\n"
        "Iltimos aniqroq yozing:\n"
        "- ЭЦП\n- IMEI\n- Паспорт\n- K-ETA\n- Иш"
    )

# MAIN HANDLER
@bot.message_handler(func=lambda message: True)
def handle(message):
    users.add(message.chat.id)
    text = message.text

    if text == "📄 ЭЦП":
        bot.send_message(message.chat.id, smart_ai("эцп"))

    elif text == "🆔 IMEI":
        bot.send_message(message.chat.id, smart_ai("imei"))

    elif text == "🛂 Паспорт":
        bot.send_message(message.chat.id, smart_ai("паспорт"))

    elif text == "✈️ K-ETA":
        bot.send_message(message.chat.id, smart_ai("k-eta"))

    elif text == "💼 Чет элда иш":
        bot.send_message(message.chat.id, smart_ai("иш"))

    elif text == "❓ Савол бериш":
        bot.send_message(message.chat.id, "эшитаман нима соволингиз бор , Фақат тепадагилар буйича совол қуйинг")
    elif "эцп" in text.lower():
        bot.send_message(message.chat.id, "📄 ЭЦП: pki.gov.kz орқали олинади")

    elif "imei" in text.lower():
        bot.send_message(message.chat.id, "🆔 IMEI: imei.rfs.gov.kz орқали текширилади")

    elif "паспорт" in text.lower():
        bot.send_message(message.chat.id, "🛂 Паспорт: eGov.kz орқали текширилади")

    elif "корея" in text.lower() or "k-eta" in text.lower():
        bot.send_message(message.chat.id, "✈️ K-ETA: Корея учун онлайн ариза")

    else:
        bot.send_message(message.chat.id, "🤖 Мен тушунмадим, бошқача ёзиб кўринг")
    

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti"

def run_bot():
    bot.infinity_polling()

def run_web():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_bot)
    t1.start()
    run_web()