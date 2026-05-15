from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import expenses, stats, categories

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Tracker API",
    description="API для учёта расходов телеграм-бота",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses.router, prefix="/expenses", tags=["Расходы"])
app.include_router(stats.router, prefix="/stats", tags=["Статистика"])
app.include_router(categories.router, prefix="/categories", tags=["Категории"])


@app.get("/")
def root():
    return {"message": "Finance Tracker API работает!"}
