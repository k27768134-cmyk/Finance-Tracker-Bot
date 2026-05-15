from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
import matplotlib.pyplot as plt
import matplotlib
import io

from keyboards.main_menu import get_main_menu
from utils.api_client import api_client

matplotlib.use("Agg")  # Без GUI

router = Router()


def generate_pie_chart(by_category: dict, total: float, month: int, year: int) -> bytes:
    """Генерирует круговую диаграмму расходов по категориям."""
    if not by_category:
        return None

    labels = list(by_category.keys())
    values = list(by_category.values())

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    colors = ["#e94560", "#0f3460", "#533483", "#e94560", "#16213e",
              "#f5a623", "#7ed321", "#4a90e2", "#9013fe"]

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        colors=colors[:len(labels)],
        textprops={"color": "white", "fontsize": 10},
        pctdistance=0.85,
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(9)

    months_ru = ["", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                 "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    ax.set_title(
        f"Расходы: {months_ru[month]} {year}\nИтого: {total:.2f} ₽",
        color="white",
        fontsize=13,
        pad=20,
    )

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf.read()


@router.message(F.text == "📊 Статистика")
async def show_stats(message: Message):
    stats = await api_client.get_monthly_stats(message.from_user.id)

    if stats["total"] == 0:
        await message.answer(
            "📭 За этот месяц расходов нет.\nДобавь первый расход!",
            reply_markup=get_main_menu(),
        )
        return

    # Текстовая статистика
    text = f"📊 *Статистика за {stats['month']}/{stats['year']}*\n\n"
    for cat, amount in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
        percent = (amount / stats["total"]) * 100
        text += f"{cat}: *{amount:.2f} ₽* ({percent:.1f}%)\n"
    text += f"\n💰 *Итого: {stats['total']:.2f} ₽*"

    await message.answer(text, parse_mode="Markdown")

    # График
    chart_bytes = generate_pie_chart(
        stats["by_category"], stats["total"], stats["month"], stats["year"]
    )
    if chart_bytes:
        photo = BufferedInputFile(chart_bytes, filename="stats.png")
        await message.answer_photo(photo, caption="📈 График расходов по категориям")


@router.message(F.text == "📋 История")
async def show_history(message: Message):
    expenses = await api_client.get_recent_expenses(message.from_user.id, limit=5)

    if not expenses:
        await message.answer("📭 Расходов пока нет.", reply_markup=get_main_menu())
        return

    text = "📋 *Последние 5 расходов:*\n\n"
    for exp in expenses:
        cat = exp["category"]
        date = exp["created_at"][:10]
        desc = f" — {exp['description']}" if exp["description"] else ""
        text += f"{cat['emoji']} {exp['amount']:.2f} ₽{desc}\n_{cat['name']} • {date}_\n\n"

    await message.answer(text, parse_mode="Markdown", reply_markup=get_main_menu())
