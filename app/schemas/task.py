from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

from app.models.task import TaskStatus

if TYPE_CHECKING:
    from app.schemas.user import User


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskInDBBase(TaskBase):
    id: int
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Task(TaskInDBBase):
    pass


class TaskWithOwner(Task):
    owner: "User"
