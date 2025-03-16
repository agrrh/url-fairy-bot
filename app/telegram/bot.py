import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from .config import config

from .telegram.handlers import start, message

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)
logger = logging.getLogger(__name__)


def start_bot():
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(message, content_types=types.ContentType.TEXT)
    executor.start_polling(dp, skip_updates=False)
