from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models import User
from app.api.dependencies import get_current_user

from app.schemas.stats import TaskStats

router = APIRouter(prefix="/stats", tags=["Stats"])

STATS_BASE_SQL = """
    select
        count(*) as total,
        count(*) filter (where status = 'TODO') as todo,
        count(*) filter (where status = 'IN_PROGRESS') as in_progress,
        count(*) filter (where status = 'QA') as qa,
        count(*) filter (where status = 'DONE') as done,
        count(*) filter (where status = 'FLAGGED') as flagged,
        count(*) filter (where priority = 'LOWEST') as lowest,
        count(*) filter (where priority = 'LOW') as low,
        count(*) filter (where priority = 'MEDIUM') as medium,
        count(*) filter (where priority = 'HIGH') as high,
        count(*) filter (where priority = 'HIGHEST') as highest,
        count(*) filter (where deadline is null) as no_deadline,
        count(*) filter (where deadline is not null) as has_deadline,
        count(*) filter (where deadline < now()) as overdue
    from tasks
"""

@router.get(
    "/all",
    response_model=TaskStats,
    status_code=status.HTTP_200_OK,
    summary="Загальна статистика по всіх задачах системи",
    description="Повертає глобальні аналітичні показники по всіх задачах у системі: розподіл за всіма 5 статусами, 5 пріоритетами, наявністю дедлайнів та простроченими термінами. Використовується для загального моніторингу на сторінці 'Про систему'.",
    response_description="Зведена агрегована статистика за всіма задачами системи",
    responses={
        200: {"description": "Статистику успішно розраховано та повернуто"},
        401: {"description": "Неавторизований доступ, потрібен дійсний токен"}
    }
)
async def get_stats_all(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = text(STATS_BASE_SQL)
    result = await db.execute(stmt)
    row = result.first()
    return row

@router.get(
    "/me",
    response_model=TaskStats,
    status_code=status.HTTP_200_OK,
    summary="Персональна статистика поточного користувача",
    description="Повертає агреговані аналітичні показники виключно за задачами, створеними поточним авторизованим користувачем (розподіл за статусами, пріоритетами, дедлайнами).",
    response_description="Персональні показники задач користувача",
    responses={
        200: {"description": "Персональну статистику успішно отримано"},
        401: {"description": "Неавторизований доступ, потрібен дійсний токен"}
    }
)
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = text(STATS_BASE_SQL + " where created_by = :user_id")
    result = await db.execute(stmt, {"user_id": current_user.user_id})
    row = result.first()
    return row