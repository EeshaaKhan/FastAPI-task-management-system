"""
CRUD package initialization.
"""
from app.crud.task import TaskCRUD, get_task_crud
from app.crud.user import UserCRUD, get_user_crud

__all__ = ["UserCRUD", "get_user_crud", "TaskCRUD", "get_task_crud"]
