from datetime import date, datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import Date, cast, or_, func

from app.db.database import get_db
from app.db.models import Task, User, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskDetailsResponse, TaskRegistryResponse, SortOrder
from app.api.dependencies import get_current_user
from app.core.logger import logger

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Створення нової задачі",
    description="Створює нову задачу для поточного автентифікованого користувача. Статус за замовчуванням — 'TODO', пріоритет — 'MEDIUM'. Творцем задачі автоматично призначається поточний користувач.",
    response_description="Успішно створена задача з присвоєним task_id",
    responses={
        201: {"description": "Задачу успішно створено"},
        401: {"description": "Неавторизований доступ"},
        422: {"description": "Помилка валідації вхідних даних"}
    }
)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    logger.info(f"Спроба створення нової задачі користувачем {current_user.email}: {task_in.model_dump_json()}")
    
    new_task = Task(**task_in.model_dump(), created_by=current_user.user_id)

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    logger.info(f"Нова задача створена: {TaskResponse.model_validate(new_task).model_dump_json()}")
    return new_task

@router.get(
    "/",
    response_model=TaskRegistryResponse,
    summary="Отримання реєстру задач (фільтрація, сортування, пагінація)",
    description="Повертає реєстр задач поточного користувача. Підтримує повнотекстовий пошук за назвою та описом, фільтрацію за статусом, пріоритетом і дедлайном, динамічне сортування за будь-яким полем та посторінкову навігацію (пагінацію).",
    response_description="Об'єкт реєстру з лічильниками total, filtered та списком знайдених рядків rows",
    responses={
        200: {"description": "Реєстр задач успішно отримано"},
        400: {"description": "Некоректні параметри пагінації чи сортування"},
        401: {"description": "Неавторизований доступ"}
    }
)
async def get_tasks(
    search: Optional[str] = Query(
        None, 
        description="Пошуковий запит (пошук підрядка в назві або описі)", 
        examples=["підпис"]
    ),
    status: Optional[TaskStatus] = Query(
        None, 
        description="Фільтр за статусом задачі", 
        examples=[TaskStatus.IN_PROGRESS]
    ),
    priority: Optional[TaskPriority] = Query(
        None, 
        description="Фільтр за пріоритетом задачі", 
        examples=[TaskPriority.HIGH]
    ),
    deadline: Optional[date] = Query(
        None, 
        description="Фільтр за точною датою дедлайну (РРРР-ММ-ДД)", 
        examples=["2026-10-31"]
    ),
    limit: Optional[int] = Query(
        default=10, 
        ge=1, 
        le=100, 
        description="Кількість задач на сторінці (від 1 до 100)", 
        examples=[10]
    ),
    page: Optional[int] = Query(
        default=1, 
        ge=1, 
        description="Номер сторінки (починається з 1)", 
        examples=[1]
    ),
    sort_by: Optional[str] = Query(
        default="created_at", 
        description="Поле для сортування (created_at, deadline, priority, status, title)", 
        examples=["created_at"]
    ),
    sort_order: Optional[SortOrder] = Query(
        default=SortOrder.DESC, 
        description="Напрямок сортування ('asc' або 'desc')", 
        examples=[SortOrder.DESC]
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if page < 1: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Сторінка має бути більшою за 0"
        )

    if limit < 1: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Ліміт має бути більшим за 0"
        )

    if sort_order not in ["asc", "desc"]: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Порядок сортування має бути 'asc' або 'desc'"
        )

    sort_field = getattr(Task, sort_by, None)
    if not sort_field: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Сортування за цим полем не підтримується"
        )
    
    order_clause = sort_field.desc() if sort_order == "desc" else sort_field.asc()
    
    offset = limit * (page - 1)
    

    base_query = select(Task).where(Task.created_by == current_user.user_id)

    total = (
        await db.execute(
            select(func.count(Task.task_id)).where(Task.created_by == current_user.user_id)
        )
    ).scalar() or 0

    query = base_query
    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if deadline:
        query = query.where(cast(Task.deadline, Date) == deadline)
    if search:
        query = query.where(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )

    filtered = (
        await db.execute(
            select(func.count()).select_from(query.subquery())
        )
    ).scalar() or 0
        
    query = query.order_by(order_clause).limit(limit).offset(offset)    

    result = await db.execute(query)

    tasks = result.scalars().all()

    return TaskRegistryResponse(
        total=total,
        filtered=filtered,
        rows=tasks
    )


@router.get(
    "/{task_id}",
    response_model=TaskDetailsResponse,
    summary="Перегляд інформації про окрему задачу",
    description="Повертає повну інформацію про задачу за її унікальним ідентифікатором (UUID). Доступ дозволено лише автору задачі.",
    responses={
        200: {"description": "Дані задачі успішно отримано"},
        401: {"description": "Неавторизований доступ"},
        403: {"description": "Заборонено: спроба перегляду чужої задачі"},
        404: {"description": "Задачу з таким ID не знайдено"}
    }
)
async def get_task(
    task_id: str = Path(
        ..., 
        description="Унікальний ідентифікатор задачі (UUIDv4)", 
        examples=["a1b2c3d4-e5f6-7890-1234-567890abcdef"]
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Task).where(Task.task_id == task_id))
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задачу не знайдено")

    if task.created_by != current_user.user_id:
        logger.warning(f"Користувач {current_user.user_id} намагався отримати чужу задачу {task_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Немає доступу до цієї задачі")

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалення задачі",
    description="Видаляє задачу за її унікальним ідентифікатором (UUID). Видалення дозволено лише користувачеві, який є автором цієї задачі.",
    responses={
        204: {"description": "Задачу успішно видалено"},
        401: {"description": "Неавторизований доступ"},
        403: {"description": "Заборонено: спроба видалення чужої задачі"},
        404: {"description": "Задачу з таким ID не знайдено"}
    }
)
async def delete_task(
    task_id: str = Path(
        ..., 
        description="Унікальний ідентифікатор задачі (UUIDv4)", 
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Task).where(Task.task_id == task_id))
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не знайдено")

    if task.created_by != current_user.user_id:
        logger.warning(f"Користувач {current_user.email} намагався видалити задачу {task_id}, яка не належить йому")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Немає прав на видалення цієї задачі")

    await db.delete(task)
    await db.commit()

    logger.info(f"Задачу {task_id} успішно видалено користувачем {current_user.email}")

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Оновлення даних задачі",
    description="Оновлює поля існуючої задачі (назва, опис, статус, пріоритет, дедлайн). Редагувати задачу має право виключно її автор.",
    response_description="Оновлений об'єкт задачі з актуальною датою updated_at",
    responses={
        200: {"description": "Задачу успішно оновлено"},
        401: {"description": "Неавторизований доступ"},
        403: {"description": "Заборонено: спроба редагування чужої задачі"},
        404: {"description": "Задачу з таким ID не знайдено"},
        422: {"description": "Помилка валідації вхідних полів"}
    }
)
async def update_task(
    task_in: TaskUpdate,
    task_id: str = Path(
        ..., 
        description="Унікальний ідентифікатор задачі (UUIDv4)", 
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    ),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"Спроба редагування задачі користувачем {current_user.email}: {task_id}")
    
    result = await db.execute(select(Task).where(Task.task_id == task_id))
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не знайдено")

    if task.created_by != current_user.user_id:
        logger.warning(f"Користувач {current_user.email} намагався редагувати задачу {task_id}, яка не належить йому")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Немає прав на редагування цієї задачі")

    task.title = task_in.title
    task.description = task_in.description
    task.status = task_in.status
    task.priority = task_in.priority
    task.deadline = task_in.deadline
    task.updated_at = datetime.now(timezone.utc)
    task.updated_by = current_user.user_id

    await db.commit()
    await db.refresh(task)

    logger.info(f"Задача {task_id} успішно оновлена користувачем {current_user.email}: {TaskResponse.model_validate(task).model_dump_json()}")

    return task