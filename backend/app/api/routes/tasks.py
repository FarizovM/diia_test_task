from datetime import date, datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import Date, cast, or_

from app.db.database import get_db
from app.db.models import Task, User, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    new_task = Task(**task_in.model_dump(), created_by=current_user.user_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    search: Optional[str] = Query(None,description="Пошуковий запит за назвою та описом"),
    status: Optional[TaskStatus] = Query(None,description="Фільтр за статусом"),
    priority: Optional[TaskPriority] = Query(None,description="Фільтр за пріоритетом"),
    deadline: Optional[date] = Query(None,description="Фільтр за дедлайном"),
    limit: Optional[int] = Query(default=10,description="Кількість задач на сторінці"),
    page: Optional[int] = Query(default=1,description="Номер сторінки",),
    sort_by: Optional[str] = Query(default="created_at",description="Сортування за полем"),
    sort_order: Optional[str] = Query(default="desc",description="Порядок сортування"),
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
    

    query = select(Task).where(Task.created_by == current_user.user_id)

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
        
    query = query.order_by(order_clause)
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)

    tasks = result.scalars().all()
    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasks not found",
        )
    return tasks

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Task).where(Task.task_id == task_id))
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не знайдено")

    if task.created_by != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Немає прав на видалення цієї задачі")

    await db.delete(task)
    await db.commit()

@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: str,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Task).where(Task.task_id == task_id))
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не знайдено")

    if task.created_by != current_user.user_id:
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
    return task