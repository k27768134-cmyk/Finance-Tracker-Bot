from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from datetime import datetime

from database import get_db
from models import Expense, Category
from schemas import MonthlyStats

router = APIRouter()


@router.get("/monthly/{user_id}", response_model=MonthlyStats)
def get_monthly_stats(
    user_id: int,
    year: int = None,
    month: int = None,
    db: Session = Depends(get_db),
):
    """Получить статистику расходов за месяц."""
    now = datetime.utcnow()
    year = year or now.year
    month = month or now.month

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id,
            extract("year", Expense.created_at) == year,
            extract("month", Expense.created_at) == month,
        )
        .all()
    )

    total = sum(e.amount for e in expenses)

    by_category: dict[str, float] = {}
    for expense in expenses:
        label = f"{expense.category.emoji} {expense.category.name}"
        by_category[label] = by_category.get(label, 0) + expense.amount

    return MonthlyStats(year=year, month=month, total=total, by_category=by_category)
