import os
import requests
import yt_dlp
from urllib.parse import urlparse, urlunparse
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID"))
CHAT_ID = int(os.getenv("CHAT_ID"))

CACHE_DIR = "video_cache"

def start(update, context):
    update.message.reply_text("Hello! I'm your bot. Send me a message!")

def follow_redirects(url):
    response = requests.head(url, allow_redirects=True)
    clean_url = urlunparse(urlparse(response.url)._replace(query=''))
    return clean_url

def sanitize_filename(filename):
    return "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in filename)

def download_tiktok_video(url):
    ydl_opts = {
        'outtmpl': os.path.join(CACHE_DIR, sanitize_filename(url) + '.mp4'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def forward_message(update, context):
    if update.message.from_user.id == USER_ID:
        message_text = update.message.text

        if message_text.startswith("http") or message_text.startswith("www"):
            clean_url = follow_redirects(message_text)

            if "tiktok" in clean_url:
                video_path = os.path.join(CACHE_DIR, sanitize_filename(clean_url) + '.mp4')
                if os.path.exists(video_path):
                    with open(video_path, "rb") as video_file:
                        context.bot.send_video(chat_id=CHAT_ID, video=video_file, caption=clean_url)
                else:
                    download_tiktok_video(clean_url)
                    with open(video_path, "rb") as video_file:
                        context.bot.send_video(chat_id=CHAT_ID, video=video_file, caption=clean_url)
            else:
                context.bot.send_message(chat_id=CHAT_ID, text=clean_url)

            update.message.reply_text("Content has been forwarded to the selected channel.")
        else:
            context.bot.send_message(chat_id=CHAT_ID, text=message_text)
            update.message.reply_text("Your message has been forwarded to the selected channel.")
    else:
        update.message.reply_text("Sorry, you are not authorized to use this bot.")

def main():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
