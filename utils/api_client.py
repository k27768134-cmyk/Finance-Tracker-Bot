import aiohttp
from config import API_BASE_URL


class APIClient:
    """Клиент для взаимодействия с FastAPI бэкендом."""

    def __init__(self):
        self.base_url = API_BASE_URL

    async def get_categories(self) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/categories/") as resp:
                return await resp.json()

    async def add_expense(self, user_id: int, amount: float, category_id: int, description: str = None) -> dict:
        payload = {
            "user_id": user_id,
            "amount": amount,
            "category_id": category_id,
            "description": description,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/expenses/", json=payload) as resp:
                return await resp.json()

    async def get_monthly_stats(self, user_id: int) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/stats/monthly/{user_id}") as resp:
                return await resp.json()

    async def get_recent_expenses(self, user_id: int, limit: int = 5) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/expenses/user/{user_id}?limit={limit}"
            ) as resp:
                return await resp.json()


api_client = APIClient()
