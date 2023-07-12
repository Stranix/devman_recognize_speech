import os
import logging

from google.cloud import dialogflow

logger = logging.getLogger('recognize_speech_bot')


def detect_intent_texts(session_id: str, text: str, language_code='ru') -> str:
    project_id = os.environ['GOOGLE_DIALOG_FLOW_ID']
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    logger.debug('Session path: %s', session)

    dialog_flow = {
        'session': session,
        'query_input': {
            'text': {
                'text': text,
                'language_code': language_code
            }
        }
    }

    response = session_client.detect_intent(request=dialog_flow)

    logger.debug('Query text: %s', response.query_result.query_text)
    logger.debug('Fulfillment: %s', response.query_result.fulfillment_text)
    logger.debug(
        'Detected intent: %s (confidence: %s)',
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence,
    )

    return response.query_result.fulfillment_text
