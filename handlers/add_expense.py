from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.categories import get_categories_keyboard
from keyboards.main_menu import get_main_menu
from utils.api_client import api_client

router = Router()


class AddExpenseForm(StatesGroup):
    """Состояния FSM для добавления расхода."""
    choosing_category = State()
    entering_amount = State()
    entering_description = State()


@router.message(F.text == "➕ Добавить расход")
async def start_add_expense(message: Message, state: FSMContext):
    categories = await api_client.get_categories()
    await message.answer(
        "Выбери категорию расхода:",
        reply_markup=get_categories_keyboard(categories),
    )
    await state.set_state(AddExpenseForm.choosing_category)
    await state.update_data(categories=categories)


@router.callback_query(AddExpenseForm.choosing_category, F.data.startswith("cat_"))
async def category_chosen(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split("_")[1])
    await state.update_data(category_id=category_id)
    await callback.message.answer("Введи сумму расхода (например: 250.50):")
    await state.set_state(AddExpenseForm.entering_amount)
    await callback.answer()


@router.message(AddExpenseForm.entering_amount)
async def amount_entered(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Введи корректную сумму, например: 150 или 99.99")
        return

    await state.update_data(amount=amount)
    await message.answer(
        "Добавь описание (необязательно).\nОтправь точку «.» чтобы пропустить:"
    )
    await state.set_state(AddExpenseForm.entering_description)


@router.message(AddExpenseForm.entering_description)
async def description_entered(message: Message, state: FSMContext):
    description = None if message.text == "." else message.text
    data = await state.get_data()

    result = await api_client.add_expense(
        user_id=message.from_user.id,
        amount=data["amount"],
        category_id=data["category_id"],
        description=description,
    )

    # Найдём название категории
    cat_name = next(
        (f"{c['emoji']} {c['name']}" for c in data["categories"] if c["id"] == data["category_id"]),
        "Категория",
    )

    await message.answer(
        f"✅ Расход добавлен!\n\n"
        f"💰 Сумма: {data['amount']:.2f} ₽\n"
        f"📁 Категория: {cat_name}\n"
        f"📝 Описание: {description or '—'}",
        reply_markup=get_main_menu(),
    )
    await state.clear()
