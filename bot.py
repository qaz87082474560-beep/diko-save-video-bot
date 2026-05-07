import telebot
import yt_dlp
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading
import os

TOKEN = "8633205145:AAFk0f-hsTgBAt9r9wb_bUMqvc9ton0zjlc"
CHANNEL_USERNAME = "@diko_vidio_save"

bot = telebot.TeleBot(TOKEN)

# MENU
menu = ReplyKeyboardMarkup(resize_keyboard=True)

btn1 = KeyboardButton("🎬 Video")
btn2 = KeyboardButton("🎵 MP3")

menu.add(btn1, btn2)

# USER MODE
mode = {}

# VIDEO DOWNLOAD
def download_video(url):

   ydl_opts = {
    'outtmpl': 'video.%(ext)s',
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'quiet': True,
    'noplaylist': True,
    'cookiefile': 'cookies.txt',
    'nocheckcertificate': True
}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# MP3 DOWNLOAD
def download_mp3(url):

    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True,
        'noplaylist': True,
        'cookiefile': 'cookies.txt'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# START
@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id

    try:

        member = bot.get_chat_member(
            CHANNEL_USERNAME,
            user_id
        )

        if member.status in ["member", "administrator", "creator"]:

            bot.send_message(
                message.chat.id,
                "🔥 Khamutbekov Video Save Bot\n\nKerakli bo‘limni tanlang 👇",
                reply_markup=menu
            )

        else:

            bot.send_message(
                message.chat.id,
                f"❌ Avval kanalga obuna bo‘ling:\n{CHANNEL_USERNAME}"
            )

    except:

        bot.send_message(
            message.chat.id,
            f"❌ Avval kanalga obuna bo‘ling:\n{CHANNEL_USERNAME}"
        )

# HANDLE
@bot.message_handler(func=lambda message: True)
def handle(message):

    text = message.text

    # VIDEO BUTTON
    if text == "🎬 Video":

        mode[message.chat.id] = "video"

        bot.send_message(
            message.chat.id,
            "📥 Video link yubor"
        )

        return

    # MP3 BUTTON
    if text == "🎵 MP3":

        mode[message.chat.id] = "mp3"

        bot.send_message(
            message.chat.id,
            "🎵 Audio link yubor"
        )

        return

    url = text

    if "http" not in url:

        bot.send_message(
            message.chat.id,
            "❌ Link yubor"
        )

        return

    # VIDEO MODE
    if mode.get(message.chat.id) == "video":

        bot.send_message(
            message.chat.id,
            "⏳ Video yuklanmoqda..."
        )

        try:

            file = download_video(url)

            size = os.path.getsize(file)

            if size > 49 * 1024 * 1024:

                bot.send_message(
                    message.chat.id,
                    "⚠️ Video juda katta"
                )

                os.remove(file)
                return

            with open(file, 'rb') as f:
                bot.send_video(message.chat.id, f)

            os.remove(file)

        except:

            bot.send_message(
                message.chat.id,
                "❌ Video ishlamadi"
            )

    # MP3 MODE
    elif mode.get(message.chat.id) == "mp3":

        bot.send_message(
            message.chat.id,
            "🎵 MP3 yuklanmoqda..."
        )

        try:

            file = download_mp3(url)

            with open(file, 'rb') as f:
                bot.send_audio(message.chat.id, f)

            os.remove(file)

        except:

            bot.send_message(
                message.chat.id,
                "❌ MP3 ishlamadi"
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
