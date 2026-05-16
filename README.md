# 💰 Finance Tracker Bot

Телеграм-бот для учёта личных расходов с FastAPI бэкендом, базой данных и графиками.

## 🚀 Возможности

- ➕ Добавление расходов с выбором категории
- 📊 Статистика за текущий месяц
- 📈 Круговой график расходов по категориям
- 📋 История последних трат
- 🗂 8 встроенных категорий (Еда, Транспорт, Развлечения и др.)

## 🏗 Архитектура

```
finance_bot/
├── bot.py                  # Точка входа бота
├── config.py               # Конфигурация (токены, URL)
├── requirements.txt
├── .env.example
│
├── handlers/               # Обработчики команд и сообщений
│   ├── start.py            # /start
│   ├── add_expense.py      # Добавление расхода (FSM)
│   └── stats.py            # Статистика и история
│
├── keyboards/              # Клавиатуры
│   ├── main_menu.py        # Главное меню
│   └── categories.py       # Инлайн-категории
│
├── utils/
│   └── api_client.py       # HTTP-клиент для FastAPI
│
└── api/                    # FastAPI бэкенд
    ├── main.py             # Приложение FastAPI
    ├── database.py         # Подключение к SQLite
    ├── models.py           # Модели SQLAlchemy
    ├── schemas.py          # Pydantic схемы
    └── routers/
        ├── expenses.py     # CRUD расходов
        ├── stats.py        # Статистика
        └── categories.py   # Категории
```


## 📡 API эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/categories/` | Список категорий |
| POST | `/categories/` | Создать категорию |
| POST | `/expenses/` | Добавить расход |
| GET | `/expenses/user/{id}` | Расходы пользователя |
| DELETE | `/expenses/{id}` | Удалить расход |
| GET | `/stats/monthly/{id}` | Статистика за месяц |

## 🛠 Технологии

- **aiogram 3** — асинхронный фреймворк для Telegram Bot API
- **FastAPI** — современный веб-фреймворк для API
- **SQLAlchemy** — ORM для работы с базой данных
- **SQLite** — база данных (файл `finance.db`)
- **Pydantic** — валидация данных
- **matplotlib** — генерация графиков
- **aiohttp** — асинхронные HTTP-запросы

## 📝 Используемые паттерны

- **FSM (Finite State Machine)** — пошаговый диалог добавления расхода
- **Dependency Injection** — передача сессии БД в FastAPI
- **Repository pattern** — разделение роутеров по сущностям
- **DTO/Schema** — Pydantic модели для валидации входных/выходных данных
