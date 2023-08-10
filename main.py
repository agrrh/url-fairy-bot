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
USER_ID = int(os.getenv("USER_ID"))
CHAT_ID = int(os.getenv("CHAT_ID"))

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

async def download_tiktok_video(url):
    ydl_opts = {
        'outtmpl': os.path.join(CACHE_DIR, sanitize_filename(url) + '.mp4'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@dp.message_handler(content_types=[types.ContentType.TEXT])
async def forward_message(message: types.Message):
    if message.from_user.id == USER_ID:
        message_text = message.text

        if message_text.startswith("http") or message_text.startswith("www"):
            clean_url = follow_redirects(message_text)

            if "tiktok" in clean_url:
                video_path = os.path.join(CACHE_DIR, sanitize_filename(clean_url) + '.mp4')
                if os.path.exists(video_path):
                    with open(video_path, "rb") as video_file:
                        await bot.send_video(message.chat.id, video_file, caption=clean_url)
                else:
                    await download_tiktok_video(clean_url)
                    with open(video_path, "rb") as video_file:
                        await bot.send_video(message.chat.id, video_file, caption=clean_url)
            else:
                await bot.send_message(message.chat.id, clean_url)

            await message.reply("Content has been forwarded to the selected channel.")
        else:
            await bot.send_message(message.chat.id, message_text)
            await message.reply("Your message has been forwarded to the selected channel.")
    else:
        await bot.send_message(message.chat.id, "Sorry, you are not authorized to use this bot.")

def main():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
