from aiogram.fsm.state import State, StatesGroup

class WeatherStates(StatesGroup):
    """Состояние для диолога о погоде"""
    waiting_city = State()