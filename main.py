import os
import requests
import yt_dlp
from urllib.parse import urlparse, urlunparse
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_IDS = os.getenv("ALLOWED_USER_IDS")
if ALLOWED_USER_IDS == "*":
    ALLOWED_USER_IDS = []  # An empty list means anyone is allowed
else:
    ALLOWED_USER_IDS = [int(id) for id in ALLOWED_USER_IDS.split(",")]

CACHE_DIR = "video_cache"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

async def start(message: types.Message):
    await message.reply("Hello! I'm your bot. Send me a message!")

def follow_redirects(url):
    response = requests.head(url, allow_redirects=True)
    clean_url = urlunparse(urlparse(response.url)._replace(query=''))
    return clean_url

def sanitize_filename(filename):
    return "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in filename)

async def yt_dlp_download(url):
    ydl_opts = {
        'outtmpl': os.path.join(CACHE_DIR, sanitize_filename(url) + '.mp4'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@dp.message_handler(content_types=[types.ContentType.TEXT])
async def forward_message(message: types.Message):
    if not ALLOWED_USER_IDS or message.from_user.id in ALLOWED_USER_IDS:
        message_text = message.text

        if message_text.startswith("http") or message_text.startswith("www"):
            clean_url = follow_redirects(message_text)

            if "tiktok" in clean_url:
                video_path = os.path.join(CACHE_DIR, sanitize_filename(clean_url) + '.mp4')
                if os.path.exists(video_path):
                    with open(video_path, "rb") as video_file:
                        await message.reply_video(video_file, caption=clean_url)
                else:
                    await yt_dlp_download(clean_url)
                    with open(video_path, "rb") as video_file:
                        await message.reply_video(video_file, caption=clean_url)
            else:
                await message.reply(clean_url)

        else:
            await message.reply(message_text)
    else:
        await message.reply("Sorry, you are not authorized to use this bot.")

def main():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
