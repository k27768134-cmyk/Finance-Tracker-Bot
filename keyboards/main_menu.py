from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню бота."""
    keyboard = [
        [KeyboardButton(text="➕ Добавить расход")],
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="📋 История")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
