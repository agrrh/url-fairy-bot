from aiogram import types


async def start(message: types.Message):
    await message.reply("Hello! Send me a URL to process!")
