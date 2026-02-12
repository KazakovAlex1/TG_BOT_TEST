import logging
import asyncio

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command

from special_scripts import clear_cache
from config import config
from states import WeatherStates, ConvertStates, TodoStates
from hendlers.comands import(
    start_cmd, help_cmd, weather_cmd, process_weather_city, 
    cancel_fsm, convert_cmd, process_convert_amount, 
    process_convert_from, process_currency_callback,
    todo_cmd, todo_add_callback, todo_clear_callback,
    todo_close_calback, todo_process_task, todo_toggle_callback,
)


logging.basicConfig(level=logging.INFO)

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()

dp.message.register(start_cmd, Command('start'))
dp.message.register(help_cmd, Command('help'))
dp.message.register(weather_cmd, Command('weather'))
dp.message.register(process_weather_city, WeatherStates.waiting_city)

dp.message.register(convert_cmd, Command('convert'))
dp.message.register(process_convert_amount, ConvertStates.waiting_summ)
dp.message.register(process_convert_from, ConvertStates.waiting_from_curr)

dp.message.register(todo_cmd, Command('todo'))
dp.message.register(todo_process_task, TodoStates.waiting_task)

dp.callback_query.register(process_currency_callback, F.data.startswith('currency_'))
dp.callback_query.register(cancel_fsm, F.data == 'cancel_fsm')
dp.callback_query.register(todo_add_callback, F.data == 'todo_add')
dp.callback_query.register(todo_clear_callback, F.data == 'todo_clear')
dp.callback_query.register(todo_close_calback, F.data == 'todo_close')
dp.callback_query.register(todo_toggle_callback, F.data.startswith('todo_toggle_'))


async def main():
    if not config.BOT_TOKEN:
        logging.error('Ошибка: не удалось получить BOT_TOKEN!')
        return
    
    logging.info('Запуск бота...')
    await dp.start_polling(bot)

if __name__ == '__main__':
    clear_cache()
    asyncio.run(main())