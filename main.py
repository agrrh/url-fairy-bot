import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("USER_ID"))
CHAT_ID = int(os.getenv("CHAT_ID"))

def start(update, context):
    update.message.reply_text("Hello! I'm your bot. Send me a message!")

def forward_message(update, context):
    if update.message.from_user.id == USER_ID:
        context.bot.send_message(chat_id=CHAT_ID, text=update.message.text)
        update.message.reply_text("Your message has been forwarded to the selected channel.")
    else:
        update.message.reply_text("Sorry, you are not authorized to use this bot.")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
