import logging
import re

from aiogram import types
from pydantic import ValidationError


from .models import URLMessage
from .url_processing import process_url_request

from .config import config

logger = logging.getLogger(__name__)


async def message(message: types.Message):
    if (
        message.chat.type in ["group", "supergroup"]
        and message.reply_to_message
    ):
        if message.reply_to_message.from_user.id == config.BOT_ID:
            await message.reply(
                "Please do not be mad at me 🥺. I am not very clever bot 👉👈"
                + "\n\n"
                + "I am very sorry if I did not help you 😢"
                + "\n\n"
                + "Sometimes I use external tools to help you, but they can "
                + "be offline or could not parse media too. "
                + "Especially if we are talking about 🤬🤬🤬🤬ing Facebook "
                + "\n\n"
                + "Please donate to "
                + "[Centre T](https://translyaciya.com/help_eng) 🫶",
                parse_mode=types.ParseMode.MARKDOWN,
            )
            return

    url_pattern = r"(https?://\S+)"
    urls = re.findall(url_pattern, message.text.strip())

    if not urls:
        if message.chat.type in ["group", "supergroup"]:
            return
        else:
            await message.reply("Please send a valid URL to process!")
            return

    for url in urls:
        try:
            url_message = URLMessage(
                url=url,
                is_group_chat=message.chat.type in ["group", "supergroup"],
            )
            result = await process_url_request(
                url_message.url, url_message.is_group_chat
            )
            if result is not None:
                await message.reply(
                    result, parse_mode=types.ParseMode.MARKDOWN
                )

        except ValidationError as e:
            logger.warning(f"Validation error for URL: {url} - {e}")
            await message.reply(f"Invalid URL provided: {e}")
