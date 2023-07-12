import os
import logging

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Updater
from telegram.ext import Filters
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackContext

load_dotenv()
logger = logging.getLogger('recognize_speech_bot')


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте!'
    )


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


if __name__ == '__main__':
    try:
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        logger.info('Старт бота')

        tg_bot_api = os.environ['TG_BOT_API']
        updater = Updater(token=tg_bot_api, use_context=True)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', start)
        echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(echo_handler)

        updater.start_polling()
    except KeyError:
        logger.critical('Переменная окружения TG_BOT_API - обязательная')
    except KeyboardInterrupt:
        logger.warning('Работа программы прервана')


