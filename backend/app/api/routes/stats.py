from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.db.database import get_db
from app.db.redis import get_redis
from app.db.models import User
from app.api.dependencies import get_current_user
from app.schemas.stats import TaskStats
from app.services.stats import (
    get_stats_all_cached,
    get_stats_user_cached,
)

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get(
    "/all",
    response_model=TaskStats,
    status_code=status.HTTP_200_OK,
    summary="Загальна статистика по всіх задачах системи",
    description="Повертає глобальні аналітичні показники по всіх задачах у системі із кешуванням у Redis: розподіл за статусами, пріоритетами, наявністю дедлайнів та простроченими термінами.",
    response_description="Зведена агрегована статистика за всіма задачами системи",
    responses={
        200: {"description": "Статистику успішно отримано (з кешу або БД)"},
        401: {"description": "Неавторизований доступ, потрібен дійсний токен"}
    }
)
async def get_stats_all(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    return await get_stats_all_cached(db=db, redis=redis)

@router.get(
    "/me",
    response_model=TaskStats,
    status_code=status.HTTP_200_OK,
    summary="Персональна статистика поточного користувача",
    description="Повертає агреговані аналітичні показники виключно за задачами поточного користувача із кешуванням у Redis.",
    response_description="Персональні показники задач користувача",
    responses={
        200: {"description": "Персональну статистику успішно отримано (з кешу або БД)"},
        401: {"description": "Неавторизований доступ, потрібен дійсний токен"}
    }
)
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    return await get_stats_user_cached(db=db, redis=redis, user_id=current_user.user_id)