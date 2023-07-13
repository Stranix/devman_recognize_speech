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
from logging_handlers import TelegramLogsHandler

logger = logging.getLogger('recognize_speech_bot')


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте!'
    )


def send_replay_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    _, message = detect_intent_texts(
        context.bot_data["dialogflow_project_id"],
        str(chat_id),
        update.message.text
    )
    context.bot.send_message(chat_id, message)


def run_tg_bot(tg_token: str, dialogflow_project_id: str):
    logger.info('Старт бота')
    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.bot_data["dialogflow_project_id"] = dialogflow_project_id

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(
        Filters.text & (~Filters.command),
        send_replay_message
    )

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    try:
        load_dotenv()
        tg_bot_token = os.environ['TG_BOT_TOKEN']
        tg_admin_id = int(os.environ['TG_ADMIN_ID'])
        dialog_flow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']

        logging.basicConfig(level=logging.ERROR)
        logger.addHandler(TelegramLogsHandler(tg_bot_token, tg_admin_id))

        run_tg_bot(tg_bot_token, dialog_flow_project_id)
    except KeyError:
        logger.critical('Заданы не все переменные окружения')
    except KeyboardInterrupt:
        logger.warning('Работа программы завершена')
    except Exception as error:
        logger.exception(error)

