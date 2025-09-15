"""
Models package initialization.
Import all models here to ensure they are registered with SQLAlchemy.
"""
from app.models.task import Task, TaskStatus
from app.models.user import User

__all__ = ["User", "Task", "TaskStatus"]
