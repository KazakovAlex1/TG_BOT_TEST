import logging
import asyncio

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command

from config import config
from states import WeatherStates
from hendlers.comands import start_cmd, help_cmd, weather_cmd, process_weather_city, cancel_fsm


logging.basicConfig(level=logging.INFO)

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()

dp.message.register(start_cmd, Command('start'))
dp.message.register(help_cmd, Command('help'))
dp.message.register(weather_cmd, Command('weather'))
dp.message.register(process_weather_city, WeatherStates.waiting_city)
dp.callback_query.register(cancel_fsm, F.data == 'cancel_fsm')


async def main():
    if not config.BOT_TOKEN:
        logging.error('Ошибка: не удалось получить BOT_TOKEN!')
        return
    
    logging.info('Запуск бота...')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())