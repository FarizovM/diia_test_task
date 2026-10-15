from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.db.models import TaskStatus, TaskPriority

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class TaskBase(BaseModel):
    title: str = Field(
        ...,
        description="Назва задачі",
        min_length=1,
        max_length=255,
        examples=["Інтеграція з Дія.Підпис"]
    )
    description: Optional[str] = Field(
        None,
        description="Детальний опис та вимоги до виконання задачі",
        examples=["Реалізувати верифікацію цифрового підпису користувача та валідацію сертифікатів."]
    )
    status: TaskStatus = Field(
        default=TaskStatus.TODO,
        description="Поточний статус задачі (TODO, IN_PROGRESS, QA, DONE, FLAGGED)",
        examples=[TaskStatus.TODO]
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        description="Рівень пріоритету задачі (LOWEST, LOW, MEDIUM, HIGH, HIGHEST)",
        examples=[TaskPriority.HIGH]
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Граничний термін виконання задачі (ISO 8601)",
        examples=["2026-10-31T18:00:00Z"]
    )

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        description="Оновлена назва задачі",
        min_length=1,
        max_length=255,
        examples=["Оновлена назва інтеграції"]
    )
    description: Optional[str] = Field(
        None,
        description="Оновлений опис задачі",
        examples=["Оновлені деталі технічного завдання"]
    )
    status: Optional[TaskStatus] = Field(
        None,
        description="Новий статус задачі",
        examples=[TaskStatus.IN_PROGRESS]
    )
    priority: Optional[TaskPriority] = Field(
        None,
        description="Новий пріоритет задачі",
        examples=[TaskPriority.HIGHEST]
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Новий дедлайн задачі (ISO 8601)",
        examples=["2026-11-05T23:59:59Z"]
    )

class TaskResponse(TaskBase):
    task_id: str = Field(
        ...,
        description="Унікальний ідентифікатор задачі (UUIDv4)",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    created_at: datetime = Field(
        ...,
        description="Дата та час створення запису в системі",
        examples=["2026-10-15T12:00:00Z"]
    )
    updated_at: datetime = Field(
        ...,
        description="Дата та час останнього редагування запису",
        examples=["2026-10-15T14:30:00Z"]
    )

    model_config = ConfigDict(from_attributes=True)

class TaskDetailsResponse(TaskResponse):
    created_by: str = Field(
        ...,
        description="ID користувача, що створив задачу",
        examples=["a1b2c3d4-e5f6-7890-1234-567890abcdef"]
    )
    updated_by: Optional[str] = Field(
        None,
        description="ID користувача, що востаннє оновив задачу",
        examples=["a1b2c3d4-e5f6-7890-1234-567890abcdef"]
    )

    model_config = ConfigDict(from_attributes=True)

class TaskRegistryResponse(BaseModel):
    total: int = Field(
        ...,
        description="Загальна кількість задач користувача в системі",
        examples=[25]
    )
    filtered: int = Field(
        ...,
        description="Кількість задач, що відповідають заданим критеріям пошуку та фільтрації",
        examples=[7]
    )
    rows: List[TaskResponse] = Field(
        ...,
        description="Список задач на поточній сторінці пагінації"
    )