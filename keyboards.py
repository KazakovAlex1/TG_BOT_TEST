from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой отмены для FSM диалогов."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text='❌ Отмена', callback_data='cancel_fsm'
        )]]
    )

def get_popular_currencies_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопками популярных валют."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🇷🇺 RUB', callback_data='currency_RUB'),
                InlineKeyboardButton(text='🇺🇸 USD', callback_data='currency_USD'),
                InlineKeyboardButton(text='🇪🇺 EUR', callback_data='currency_EUR')
            ],
            [
                InlineKeyboardButton(text='🇰🇿 KZT', callback_data='currency_KZT'),
                InlineKeyboardButton(text='🇨🇳 CNY', callback_data='currency_CNY'),
                InlineKeyboardButton(text='🇹🇷 TRY', callback_data='currency_TRY')
            ],
            [
                InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_fsm')
            ]
        ]
    )

def get_todo_keyboard() -> InlineKeyboardMarkup:
    """Главная клавиатура для управления списком дел."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='➕ Добавить задачу', callback_data='todo_add')
            ],
            [
                InlineKeyboardButton(text='🗑 Очистить все', callback_data='todo_clear')
            ],
            [
                InlineKeyboardButton(text='❌ Закрыть', callback_data='todo_close')
            ]
        ]
    )

def get_tasks_keyboard(task : list, user_id : int) -> InlineKeyboardMarkup:
    """Динамическая клавиатура со списком задач.
    Каждая задача — кнопка для отметки выполнения."""
    keyboard = []

    for task_id, task_text, is_done in task:
        status = '✅' if is_done else '⬜'
        button_text = f'{status} {task_text[:30]}{'...' if len(task_text) > 30 else ''}'

        callback = f'todo_toggle_{task_id}'
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=callback)])
    
    keyboard.append(
        [
            InlineKeyboardButton(text='➕ Добавить задачу', callback_data='todo_add'),
            InlineKeyboardButton(text='🗑 Очистить все', callback_data='todo_clear')
        ]
    )
    keyboard.append([InlineKeyboardButton(text='❌ Закрыть', callback_data='todo_close')])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)