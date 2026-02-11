from aiogram.fsm.state import State, StatesGroup

class WeatherStates(StatesGroup):
    """Состояние для диолога о погоде"""
    waiting_city = State()


class ConvertStates(StatesGroup):
    """Состояния для конвертации"""
    waiting_summ = State()
    waiting_from_curr = State()
    waiting_to_curr = State()