import os

from telegram.ext import CommandHandler
from telegram.ext import Updater


# pip install python-telegram-bot


def hello(update, context):
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


# Bot name: kevin3399_bot
TELEGRAM_BOT_API_KEY = os.getenv('TELEGRAM_BOT_API_KEY')
updater = Updater(TELEGRAM_BOT_API_KEY)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
