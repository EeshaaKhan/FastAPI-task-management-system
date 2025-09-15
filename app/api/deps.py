from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import get_task_crud, get_user_crud


def get_user_crud_dep(db: Session = Depends(get_db)):
    return get_user_crud(db)


def get_task_crud_dep(db: Session = Depends(get_db)):
    return get_task_crud(db)
