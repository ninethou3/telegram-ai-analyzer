import os
from dotenv import load_dotenv
from json_storage import JSONStorage
from rag_processor import RAGProcessor

load_dotenv()

class Config:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')

        # Инициализация компонентов
        self.storage = JSONStorage()
        self.rag = RAGProcessor(self.storage)

        # Настройки
        self.default_channel = "spydell_finance"
        self.deepseek_base_url = "https://api.deepseek.com/v1"

        # Валидация
        self._validate()

    def _validate(self):
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN не установлен")
        if not self.chat_id:
            raise ValueError("TELEGRAM_CHAT_ID не установлен")
        if not self.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY не установлен")