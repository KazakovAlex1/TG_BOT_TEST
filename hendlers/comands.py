import logging

from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import WeatherStates
from utils.weather import get_weather


async def start_cmd(message : Message):
    logging.info(f'Пользователь {message.from_user.first_name} вызвал команду /start')

    await message.answer('Привет я утилитарный бот!')

async def weather_cmd(message : Message, state : FSMContext):
    logging.info(f'Пользователь {message.from_user.first_name} вызвал команду /weather')

    await state.set_state(WeatherStates.waiting_city)
    await message.answer('Введите город:')

async def process_weather_city(message : Message, state : FSMContext):
    """Обработка города"""
    city = message.text.strip()
    user = message.from_user

    logging.info(f'Город {city} от {user.first_name}.')

    await message.bot.send_chat_action(message.chat.id, 'typing')

    weather_result = await get_weather(city)

    await state.clear()
    
    await message.answer(weather_result)


async def help_cmd(message : Message):
    logging.info(f'Пользователь {message.from_user.first_name} вызвал команду /help')

    await message.answer(
        "Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Помощь\n"
        "/weather - Узнать погоду\n"
        "/convert - Конвертировать валюту\n"
        "/todo - Список дел"
    )