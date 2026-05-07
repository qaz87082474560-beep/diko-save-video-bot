import telebot
import yt_dlp
from flask import Flask
import threading
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8633205145:AAFk0f-hsTgBAt9r9wb_bUMqvc9ton0zjlc"

bot = telebot.TeleBot(TOKEN)

# MENU
menu = ReplyKeyboardMarkup(resize_keyboard=True)

btn1 = KeyboardButton("🎬 Video")
btn2 = KeyboardButton("🎵 MP3")

menu.add(btn1, btn2)

mode = {}

# DOWNLOAD VIDEO
def download_video(url):

    ydl_opts = {
        'outtmpl': 'vidio.%(ext)s',
        'format' : 'best',
        'noplaylist': True,
        'qyiet': True,
        'cookiefile': 'cookeis.txt'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# DOWNLOAD MP3
def download_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)

    return "audio.mp3"
# START
@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        "🔥 KHAMUTBEKOV VIDIO SAVE BOT\n\nKerakli bo‘limni tanlang 👇",
        reply_markup=menu
    )

# HANDLE
@bot.message_handler(func=lambda message: True)
def handle(message):

    text = message.text

    # VIDEO MODE
    if text == "🎬 Video":

        mode[message.chat.id] = "video"

        bot.send_message(
            message.chat.id,
            "📥 Video link yubor"
        )
        return

    # MP3 MODE
    if text == "🎵 MP3":

        mode[message.chat.id] = "mp3"

        bot.send_message(
            message.chat.id,
            "🎵 YouTube link yubor"
        )
        return

    # CHECK LINK
    if "http" not in text:

        bot.send_message(
            message.chat.id,
            "❌ Link yubor"
        )
        return

    # MP3 DOWNLOAD
    if mode.get(message.chat.id) == "mp3":

        bot.send_message(
            message.chat.id,
            "🎵 MP3 yuklanmoqda..."
        )

        try:

            file = download_mp3(text)

            with open(file, 'rb') as f:
                bot.send_audio(message.chat.id, f)

            os.remove(file)

        except:

            bot.send_message(
                message.chat.id,
                "❌ MP3 ishlamadi"
            )

        return

    # VIDEO DOWNLOAD
    bot.send_message(
        message.chat.id,
        "⏳ Video yuklanmoqda..."
    )

    try:

        file = download_video(text)

        size = os.path.getsize(file)

        if size > 49 * 1024 * 1024:

            bot.send_message(
                message.chat.id,
                "⚠️ Video juda katta (>50MB)"
            )

            os.remove(file)
            return

        with open(file, 'rb') as f:
            bot.send_video(message.chat.id, f)

        os.remove(file)

    except:

        bot.send_message(
            message.chat.id,
            "❌ Link ishlamadi"
        )

# FLASK
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti"

def run_bot():
    bot.infinity_polling()

def run_web():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":

    threading.Thread(target=run_bot).start()

    run_web()
