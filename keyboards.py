from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой отмены для FSM диалогов."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text='❌ Отмена', callback_data='cancel_fsm'
        )]]
    )