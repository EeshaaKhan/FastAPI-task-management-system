"""
CRUD operations for Task model.
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskStatusUpdate, TaskUpdate
from app.utils.exceptions import NotFoundError


class TaskCRUD:
    """CRUD operations for Task model."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, task_data: TaskCreate, user_id: int) -> Task:
        """Create a new task for a user."""
        # Verify user exists
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")

        task = Task(title=task_data.title, description=task_data.description, user_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks for a specific user with pagination."""
        return self.db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()

    def get_by_status(self, user_id: int, status: TaskStatus) -> List[Task]:
        """Get tasks by status for a specific user."""
        return self.db.query(Task).filter(Task.user_id == user_id, Task.status == status).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Task]:
        """Get all tasks with pagination."""
        return self.db.query(Task).offset(skip).limit(limit).all()

    def update(self, task_id: int, task_data: TaskUpdate) -> Task:
        """Update an existing task."""
        task = self.get_by_id(task_id)
        if not task:
            raise NotFoundError(f"Task with id {task_id} not found")

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        self.db.commit()
        self.db.refresh(task)
        return task

    def update_status(self, task_id: int, status_data: TaskStatusUpdate) -> Task:
        """Update task status."""
        task = self.get_by_id(task_id)
        if not task:
            raise NotFoundError(f"Task with id {task_id} not found")

        task.status = status_data.status
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task."""
        task = self.get_by_id(task_id)
        if not task:
            raise NotFoundError(f"Task with id {task_id} not found")

        self.db.delete(task)
        self.db.commit()
        return True

    def count_by_user(self, user_id: int) -> int:
        """Get total number of tasks for a user."""
        return self.db.query(Task).filter(Task.user_id == user_id).count()

    def count_by_status(self, user_id: int, status: TaskStatus) -> int:
        """Get count of tasks by status for a user."""
        return self.db.query(Task).filter(Task.user_id == user_id, Task.status == status).count()


def get_task_crud(db: Session) -> TaskCRUD:
    """Factory function to get TaskCRUD instance."""
    return TaskCRUD(db)
