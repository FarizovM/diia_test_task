from pydantic import BaseModel, ConfigDict

class TaskStats(BaseModel):
    total: int
    todo: int
    in_progress: int
    qa: int
    done: int
    flagged: int
    lowest: int
    low: int
    medium: int
    high: int
    highest: int
    no_deadline: int
    has_deadline: int
    overdue: int

    model_config = ConfigDict(from_attributes=True)
