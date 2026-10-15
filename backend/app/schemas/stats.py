from pydantic import BaseModel, ConfigDict, Field

class TaskStats(BaseModel):
    total: int = Field(..., description="Загальна кількість задач у системі", examples=[20])
    todo: int = Field(..., description="Кількість задач у статусі 'До виконання' (TODO)", examples=[5])
    in_progress: int = Field(..., description="Кількість задач у статусі 'В роботі' (IN_PROGRESS)", examples=[4])
    qa: int = Field(..., description="Кількість задач у статусі 'На перевірці' (QA)", examples=[3])
    done: int = Field(..., description="Кількість задач у статусі 'Виконано' (DONE)", examples=[7])
    flagged: int = Field(..., description="Кількість задач у статусі 'Заблоковано' (FLAGGED)", examples=[1])
    lowest: int = Field(..., description="Кількість задач із пріоритетом 'Найнижчий' (LOWEST)", examples=[2])
    low: int = Field(..., description="Кількість задач із пріоритетом 'Низький' (LOW)", examples=[4])
    medium: int = Field(..., description="Кількість задач із пріоритетом 'Середній' (MEDIUM)", examples=[8])
    high: int = Field(..., description="Кількість задач із пріоритетом 'Високий' (HIGH)", examples=[4])
    highest: int = Field(..., description="Кількість задач із пріоритетом 'Найвищий' (HIGHEST)", examples=[2])
    no_deadline: int = Field(..., description="Кількість задач без встановленого дедлайну", examples=[6])
    has_deadline: int = Field(..., description="Кількість задач зі встановленим дедлайном", examples=[14])
    overdue: int = Field(..., description="Кількість задач із простроченим дедлайном", examples=[2])

    model_config = ConfigDict(from_attributes=True)
