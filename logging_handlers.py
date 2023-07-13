import logging

from telegram import Bot


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_token: str, chat_id: int):
        super().__init__()
        self.bot = Bot(token=tg_token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.chat_id, log_entry)
