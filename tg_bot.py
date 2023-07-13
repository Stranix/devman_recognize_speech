import os
import logging

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackContext
)

from dialogflow import detect_intent_texts

load_dotenv()
logger = logging.getLogger('recognize_speech_bot')


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте!'
    )


def echo(update: Update, context: CallbackContext):
    dialog_flow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']
    chat_id = update.effective_chat.id
    _, message = detect_intent_texts(
        dialog_flow_project_id,
        str(chat_id),
        update.message.text
    )
    context.bot.send_message(chat_id, message)


if __name__ == '__main__':
    try:
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG
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
        logger.critical('Заданы не все переменные окружения')
    except KeyboardInterrupt:
        logger.info('Работа программы завершена')