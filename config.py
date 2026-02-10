from os import getenv
import os


from dotenv import load_dotenv
from dataclasses import dataclass
import logging


logging.basicConfig(level=logging.INFO)

load_dotenv()

@dataclass
class Config:
    """Конфигурация приложения. Загружает настройки из .env файла."""

    BOT_TOKEN : str = ''
    WEATHER_API_KEY : str = 'a1875c4bf8792e2e0f99c731f40cf99d'
    CURRENCY_API_URL : str = ''

    def __post_init__(self):
        if not self.BOT_TOKEN:
            self.BOT_TOKEN = getenv('BOT_TOKEN', '')
    
        if not self.WEATHER_API_KEY:
            self.WEATHER_API_KEY = getenv('WEATHER_API_KEY', '')
        
        if not self.CURRENCY_API_URL:
            self.CURRENCY_API_URL = getenv('CURRENCY_API_URL', '')

        if not self.BOT_TOKEN:
            logging.warning('ВНИМАНИЕ: BOT_TOKEN не найден в .env файле!')

        if not self.WEATHER_API_KEY:
            logging.warning('ВНИМАНИЕ: WEATHER_API_KEY не найден в .env файле!')

        if not self.CURRENCY_API_URL:
            logging.warning('ВНИМАНИЕ: CURRENCY_API_URL не найден в .env файле!')

config = Config()
