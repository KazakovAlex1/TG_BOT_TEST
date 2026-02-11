import logging

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import WeatherStates, ConvertStates
from utils.weather import get_weather
from keyboards import get_cancel_keyboard
from utils.currency import convert_currency


async def start_cmd(message : Message):
    logging.info(f'Пользователь {message.from_user.first_name} вызвал команду /start')

    await message.answer('Привет я утилитарный бот!')

async def weather_cmd(message : Message, state : FSMContext):
    logging.info(f'Пользователь {message.from_user.first_name} вызвал команду /weather')

    await state.set_state(WeatherStates.waiting_city)
    await message.answer('Введите город:', reply_markup=get_cancel_keyboard())

async def process_weather_city(message : Message, state : FSMContext):
    """Обработка города"""
    city = message.text.strip()
    user = message.from_user

    logging.info(f'Город {city} от {user.first_name}.')

    await message.bot.send_chat_action(message.chat.id, 'typing')

    weather_result = await get_weather(city)

    await state.clear()
    
    await message.answer(weather_result)


async def cancel_fsm(calback : CallbackQuery, state : FSMContext):
    """Обработка отмены любого FSM диалога."""
    await state.clear()
    await calback.message.edit_text('❌ Действие отменено')
    await calback.answer()


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


async def convert_cmd(message : Message, state : FSMContext):
    """Начало диалога конвертации - запрос суммы."""
    logging.info(f'Пользователь {message.from_user.first_name} вызвал команду /convert')

    await state.set_state(ConvertStates.waiting_summ)
    await message.answer('💰 Введите сумму для конвертации:', reply_markup=get_cancel_keyboard())

    
async def process_convert_amount(message : Message, state : FSMContext):
    """Обработка введенной суммы."""
    try:
        amount = float(message.text.strip())

        if amount <= 0:
            await message.answer('❌ Сумма должна быть больше нуля. Попробуйте снова:')
            return
            
        await state.update_data(amount=amount)
        await state.set_state(ConvertStates.waiting_from_curr)
        await message.answer('💰 Из какой валюты? (например: USD, EUR, RUB)', reply_markup=get_cancel_keyboard())

    except ValueError:
        await message.answer('❌ Пожалуйста, введите число:')
    

async def process_convert_from(message : Message, state : FSMContext):
    currency = message.text.strip().upper()

    await state.update_data(for_cur=currency)
    await state.set_state(ConvertStates.waiting_to_curr)
    await message.answer('💰 В какую валюту конвертировать? (например: USD, EUR, RUB)', reply_markup=get_cancel_keyboard())


async def process_convert_to(message : Message, state : FSMContext):
    to_curr = message.text.strip().upper()

    await message.bot.send_chat_action(message.chat.id, 'typing')

    data = await state.get_data()
    amount = data.get('amount')
    from_curr = data.get('for_cur')

    result = await convert_currency(amount, from_curr, to_curr)
    await state.clear()
    await message.answer(result)