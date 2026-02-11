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
                InlineKeyboardButton(text='RUB', callback_data='currency_RUB'),
                InlineKeyboardButton(text='USD', callback_data='currency_USD'),
                InlineKeyboardButton(text='EUR', callback_data='currency_EUR')
            ],
            [
                InlineKeyboardButton(text='KZT', callback_data='currency_KZT'),
                InlineKeyboardButton(text='CNY', callback_data='currency_CNY'),
                InlineKeyboardButton(text='TRY', callback_data='currency_TRY')
            ],
            [
                InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_fsm')
            ]
        ]
    )