from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_categories_keyboard(categories: list) -> InlineKeyboardMarkup:
    """Инлайн-клавиатура с категориями."""
    buttons = [
        [InlineKeyboardButton(
            text=f"{cat['emoji']} {cat['name']}",
            callback_data=f"cat_{cat['id']}"
        )]
        for cat in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
