import os
import random

import vk_api as vk

from vk_api.longpoll import VkLongPoll, Event
from vk_api.longpoll import VkEventType

from dotenv import load_dotenv
from vk_api.vk_api import VkApiMethod

from dialogflow import detect_intent_texts

load_dotenv()


def echo(event: Event, vk_api: VkApiMethod, dialog_flow_project_id: str):
    chat_id = event.user_id
    is_fallback, message = detect_intent_texts(
        dialog_flow_project_id,
        str(chat_id),
        event.text
    )

    if is_fallback:
        return

    random_id = random.randint(1, 1000)
    vk_api.messages.send(user_id=chat_id, message=message, random_id=random_id)


if __name__ == '__main__':
    dialog_flow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']
    vk_group_token = os.environ['VK_GROUP_API_KEY']
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, dialog_flow_project_id)
