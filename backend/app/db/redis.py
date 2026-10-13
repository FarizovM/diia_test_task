import redis.asyncio as redis
from app.core.config import settings

# Створюємо пул з'єднань
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_redis():
    """Залежність для отримання клієнта Redis"""
    yield redis_client