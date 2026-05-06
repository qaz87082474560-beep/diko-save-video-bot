import telebot
import yt_dlp
from flask import Flask
import threading
import os

TOKEN = "8633205145:AAFk0f-hsTgBAt9r9wb_bUMqvc9ton0zjlc"

bot = telebot.TeleBot(TOKEN)

# --- DOWNLOAD ---
def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best',
        'noplaylist': True,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# --- START ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎬 Video link yubor (YouTube / TikTok / Instagram)"
    )

# --- HANDLE ---
@bot.message_handler(func=lambda message: True)
def handle(message):
    url = message.text

    if "http" not in url:
        bot.send_message(message.chat.id, "❌ Link yubor")
        return

    bot.send_message(message.chat.id, "⏳ Yuklanmoqda...")

    try:
        file = download_video(url)

        size = os.path.getsize(file)

        if size > 49 * 1024 * 1024:
            bot.send_message(message.chat.id, "⚠️ Video juda katta (>50MB)")
            os.remove(file)
            return

        with open(file, 'rb') as f:
            bot.send_video(message.chat.id, f)

        os.remove(file)

    except:
        bot.send_message(message.chat.id, "❌ Link ishlamadi")

# --- FLASK (24/7) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Video bot ishlayapti"

def run_bot():
    bot.infinity_polling()

def run_web():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()
    
