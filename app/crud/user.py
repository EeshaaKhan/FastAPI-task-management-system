from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.exceptions import DuplicateError, NotFoundError


class UserCRUD:
    """CRUD operations for User model."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user_data: UserCreate) -> User:
        """Create a new user and commit immediately."""
        user = User(name=user_data.name, email=user_data.email)
        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise DuplicateError(f"User with email '{user_data.email}' already exists")

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def update(self, user_id: int, user_data: UserUpdate) -> User:
        user = self.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")
        self.db.delete(user)
        self.db.commit()
        return True

    def count(self) -> int:
        return self.db.query(User).count()


def get_user_crud(db: Session) -> UserCRUD:
    return UserCRUD(db)
