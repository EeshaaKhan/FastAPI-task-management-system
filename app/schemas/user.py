from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from app.schemas.task import Task


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(...)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserWithTasks(User):
    tasks: List["Task"] = []
