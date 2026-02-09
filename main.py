import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message

from config import config

logging.basicConfig(level=logging.INFO)

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_cmd(message : Message):
    logging.info(f'Пользователь {message.from_user.first_name} вызвал команду /start')

    await message.answer('Привет я утилитарный бот!')

@dp.message(Command('weather'))
async def weather_cmd(message : Message):
    logging.info(f'Пользователь {message.from_user.first_name} вызвал команду /weather')

    await message.answer('Функция погода в разработке. Скоро будет доступна!')

@dp.message(Command('help'))
async def help_cmd(message : Message):
    logging.info(f'Пользователь {message.from_user.first_name} вызвал команду /help')

    await message.answer('Доступные команды:\n'
                         '/start - Начать работу\n' \
                         '/help - Список доступных команд\n' \
                         '/weather - Узнать погоду\n' \
                         '/convert - Конвертировать валюту\n' \
                         '/todo - Список дел')


async def main():
    if not config.BOT_TOKEN:
        logging.error('Ошибка: не удалось получить BOT_TOKEN!')
        return
    
    logging.info('Запуск бота...')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())