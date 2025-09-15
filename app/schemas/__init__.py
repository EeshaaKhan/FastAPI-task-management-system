"""
Schemas package initialization.
"""

from app.schemas.task import Task, TaskCreate, TaskStatusUpdate, TaskUpdate, TaskWithOwner
from app.schemas.user import User, UserCreate, UserUpdate, UserWithTasks

# Resolve forward references AFTER all imports
UserWithTasks.model_rebuild()
TaskWithOwner.model_rebuild()

__all__ = [
    "User",
    "UserCreate",
    "UserUpdate",
    "UserWithTasks",
    "Task",
    "TaskCreate",
    "TaskUpdate",
    "TaskStatusUpdate",
    "TaskWithOwner",
]
