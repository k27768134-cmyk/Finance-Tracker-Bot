from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Category
from schemas import CategoryCreate, CategoryResponse

router = APIRouter()

DEFAULT_CATEGORIES = [
    {"name": "Еда", "emoji": "🍔"},
    {"name": "Транспорт", "emoji": "🚗"},
    {"name": "Развлечения", "emoji": "🎮"},
    {"name": "Здоровье", "emoji": "💊"},
    {"name": "Одежда", "emoji": "👕"},
    {"name": "Связь", "emoji": "📱"},
    {"name": "Образование", "emoji": "📚"},
    {"name": "Прочее", "emoji": "💸"},
]


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Получить все категории."""
    categories = db.query(Category).all()

    # Заполняем дефолтные категории при первом запросе
    if not categories:
        for cat in DEFAULT_CATEGORIES:
            db.add(Category(**cat))
        db.commit()
        categories = db.query(Category).all()

    return categories


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию."""
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Категория уже существует")

    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
