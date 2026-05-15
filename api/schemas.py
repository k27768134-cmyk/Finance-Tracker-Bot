from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    emoji: str = "💰"


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    user_id: int
    amount: float = Field(gt=0, description="Сумма расхода, должна быть > 0")
    description: Optional[str] = None
    category_id: int


class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    description: Optional[str]
    category: CategoryResponse
    created_at: datetime

    class Config:
        from_attributes = True


class MonthlyStats(BaseModel):
    year: int
    month: int
    total: float
    by_category: dict[str, float]
