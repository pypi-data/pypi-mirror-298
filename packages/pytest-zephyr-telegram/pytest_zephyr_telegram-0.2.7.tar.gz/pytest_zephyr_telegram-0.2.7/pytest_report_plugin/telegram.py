from telebot import TeleBot


class TelegramReporter:
    enabled: bool
    topic_number: int
    enabled: bool
    chat_id: str
    bot: TeleBot

    @classmethod
    def setup(cls, set_enabled, telegram_id, telegram_token):
        cls.enabled = set_enabled
        cls.chat_id = telegram_id
        cls.bot = TeleBot(telegram_token, parse_mode="HTML")
