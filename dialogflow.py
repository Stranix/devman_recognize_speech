import os
import json
import argparse
import logging

from dotenv import load_dotenv
from google.cloud import dialogflow

logger = logging.getLogger(__name__)


def create_arg_parser():
    description = 'Работаем с Google Dialog Flow'
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('--json', '-j', default='./questions.json',
                            metavar='', type=str,
                            help='''путь до json файла с тренеровочными фразами
                            и ответами'''
                            )

    return arg_parser


def detect_intent_texts(
        project_id: str,
        session_id: str,
        text: str,
        language_code='ru'
) -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={
            'session': session,
            'query_input': query_input,
        }
    )

    return response.query_result.fulfillment_text


def create_intent(
        project_id: str,
        display_name: str,
        questions: list,
        answers: list
):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []

    for question in questions:
        part = dialogflow.Intent.TrainingPhrase.Part(text=question)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=answers)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )
    intents_client.create_intent(request={'parent': parent, 'intent': intent})


if __name__ == '__main__':
    try:
        load_dotenv()
        args = create_arg_parser().parse_args()
        filename = args.json
        dialog_flow_project_id = os.environ['DIALOGFLOW_PROJECT_ID']
        with open(filename, 'r', encoding='utf-8') as json_file:
            intents = json.loads(json_file.read())

        for intent, texts in intents.items():
            create_intent(
                dialog_flow_project_id,
                intent,
                texts['questions'],
                [texts['answer']]
            )
    except FileNotFoundError:
        logger.critical('Не нашел файл с тренеровочными фразами и ответами')
    except KeyError:
        logger.critical('Не задана переменная окружения DIALOGFLOW_PROJECT_ID')
    except KeyboardInterrupt:
        logger.warning('Работа программы прервана')
