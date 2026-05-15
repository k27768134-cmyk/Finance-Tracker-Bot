from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import get_main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я помогу тебе отслеживать расходы 💰\n\n"
        "Что умею:\n"
        "➕ Добавлять расходы по категориям\n"
        "📊 Показывать статистику за месяц\n"
        "📈 Строить графики трат\n\n"
        "Выбери действие:",
        reply_markup=get_main_menu(),
    )
