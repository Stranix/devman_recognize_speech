import os
import random
import logging

import vk_api as vk

from vk_api.vk_api import VkApiMethod
from vk_api.longpoll import Event
from vk_api.longpoll import VkLongPoll
from vk_api.longpoll import VkEventType

from dotenv import load_dotenv

from dialogflow import detect_intent_texts
from logging_handlers import TelegramLogsHandler

logger = logging.getLogger(__name__)


def send_replay_message(
        event: Event,
        vk_api: VkApiMethod,
        dialogflow_project_id: str
):
    logger.info('Отправка ответа пользователю')
    chat_id = event.user_id
    is_fallback, message = detect_intent_texts(
        dialogflow_project_id,
        str(chat_id),
        event.text
    )

    if is_fallback:
        return

    random_id = random.randint(1, 1000)
    vk_api.messages.send(user_id=chat_id, message=message, random_id=random_id)


def start_bot(vk_token: str, dialogflow_project_id: str):
    logger.info('Старт бота группы vk')
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_replay_message(event, vk_api, dialogflow_project_id)


if __name__ == '__main__':
    try:
        load_dotenv()
        dialogflow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']
        vk_group_token = os.environ['VK_GROUP_API_KEY']
        tg_bot_token = os.environ['TG_BOT_TOKEN']
        tg_admin_id = int(os.environ['TG_ADMIN_ID'])

        logging.basicConfig(level=logging.ERROR)
        logger.addHandler(TelegramLogsHandler(tg_bot_token, tg_admin_id))

        start_bot(vk_group_token, dialogflow_project_id)
    except KeyError:
        logger.critical('Не все переменные окружения заданы')
    except KeyboardInterrupt:
        logger.warning('Работа программы прервана')
    except Exception as error:
        logger.exception(error)
