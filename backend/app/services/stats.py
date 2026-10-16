from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.schemas.stats import TaskStats
from app.core.logger import logger

STATS_ALL_KEY = "stats:all"
STATS_USER_KEY_PREFIX = "stats:user:"
STATS_CACHE_TTL = 600  # 10 хвилин

def get_stats_user_key(user_id: str) -> str:
    return f"{STATS_USER_KEY_PREFIX}{user_id}"

STATS_BASE_SQL = """
    select
        count(*) as total,
        count(*) filter (where upper(cast(status as text)) = 'TODO') as todo,
        count(*) filter (where upper(cast(status as text)) = 'IN_PROGRESS') as in_progress,
        count(*) filter (where upper(cast(status as text)) = 'QA') as qa,
        count(*) filter (where upper(cast(status as text)) = 'DONE') as done,
        count(*) filter (where upper(cast(status as text)) = 'FLAGGED') as flagged,
        count(*) filter (where upper(cast(priority as text)) = 'LOWEST') as lowest,
        count(*) filter (where upper(cast(priority as text)) = 'LOW') as low,
        count(*) filter (where upper(cast(priority as text)) = 'MEDIUM') as medium,
        count(*) filter (where upper(cast(priority as text)) = 'HIGH') as high,
        count(*) filter (where upper(cast(priority as text)) = 'HIGHEST') as highest,
        count(*) filter (where deadline is null) as no_deadline,
        count(*) filter (where deadline is not null) as has_deadline,
        count(*) filter (where deadline < :now_val and upper(cast(status as text)) != 'DONE') as overdue
    from tasks
"""

async def calculate_stats_all(db: AsyncSession) -> TaskStats:
    """Обчислення глобальної статистики напряму з бази даних"""
    stmt = text(STATS_BASE_SQL)
    result = await db.execute(stmt, {"now_val": datetime.now(timezone.utc)})
    row = result.mappings().first()
    return TaskStats(**dict(row))

async def calculate_stats_user(db: AsyncSession, user_id: str) -> TaskStats:
    """Обчислення статистики конкретного користувача напряму з бази даних"""
    stmt = text(STATS_BASE_SQL + " where created_by = :user_id")
    result = await db.execute(stmt, {"now_val": datetime.now(timezone.utc), "user_id": user_id})
    row = result.mappings().first()
    return TaskStats(**dict(row))

async def get_stats_all_cached(db: AsyncSession, redis: Redis) -> TaskStats:
    """Отримання глобальної статистики з кешу Redis (Cache-Aside pattern)"""
    try:
        cached = await redis.get(STATS_ALL_KEY)
        if cached:
            logger.info("Глобальну статистику /stats/all отримано з кешу Redis")
            return TaskStats.model_validate_json(cached)
    except Exception as e:
        logger.warning(f"Помилка читання кешу stats:all з Redis: {e}")

    stats = await calculate_stats_all(db)

    try:
        await redis.setex(STATS_ALL_KEY, STATS_CACHE_TTL, stats.model_dump_json())
    except Exception as e:
        logger.warning(f"Помилка збереження кешу stats:all в Redis: {e}")

    return stats

async def get_stats_user_cached(db: AsyncSession, redis: Redis, user_id: str) -> TaskStats:
    """Отримання персональної статистики користувача з кешу Redis"""
    key = get_stats_user_key(user_id)
    try:
        cached = await redis.get(key)
        if cached:
            logger.info(f"Персональну статистику /stats/me для {user_id} отримано з кешу Redis")
            return TaskStats.model_validate_json(cached)
    except Exception as e:
        logger.warning(f"Помилка читання кешу {key} з Redis: {e}")

    stats = await calculate_stats_user(db, user_id)

    try:
        await redis.setex(key, STATS_CACHE_TTL, stats.model_dump_json())
    except Exception as e:
        logger.warning(f"Помилка збереження кешу {key} в Redis: {e}")

    return stats

async def update_stats_cache(db: AsyncSession, redis: Redis, user_id: str) -> None:
    """
    Оновлення кешу статистики в Redis при мутаціях задач (створення, редагування, видалення).
    Оновлює як загальну статистику системи, так і персональну статистику автора задачі.
    """
    try:
        stats_all = await calculate_stats_all(db)
        await redis.setex(STATS_ALL_KEY, STATS_CACHE_TTL, stats_all.model_dump_json())

        stats_user = await calculate_stats_user(db, user_id)
        await redis.setex(get_stats_user_key(user_id), STATS_CACHE_TTL, stats_user.model_dump_json())

        logger.info(f"Кеш статистики в Redis успішно оновлено для користувача {user_id} та stats:all")
    except Exception as e:
        logger.warning(f"Не вдалося оновити кеш статистики в Redis: {e}")
