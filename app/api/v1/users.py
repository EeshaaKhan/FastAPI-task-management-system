"""
app/api/v1/users.py
User API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import get_user_crud
from app.schemas import User, UserCreate, UserUpdate, UserWithTasks
from app.utils.exceptions import DuplicateError, NotFoundError

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> User:
    """
    Create a new user.
    
    Args:
        user_data: User creation data
        db: Database session
        
    Returns:
        Created user
        
    Raises:
        HTTPException: If user with email already exists
    """
    try:
        user_crud = get_user_crud(db)
        return user_crud.create(user_data)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("/", response_model=List[User])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[User]:
    """
    Get all users with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of users
    """
    user_crud = get_user_crud(db)
    return user_crud.get_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> User:
    """
    Get user by ID.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        User data
        
    Raises:
        HTTPException: If user not found
    """
    user_crud = get_user_crud(db)
    user = user_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.get("/{user_id}/with-tasks", response_model=UserWithTasks)
def get_user_with_tasks(
    user_id: int,
    db: Session = Depends(get_db)
) -> UserWithTasks:
    """
    Get user by ID with their tasks.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        User data with tasks
        
    Raises:
        HTTPException: If user not found
    """
    user_crud = get_user_crud(db)
    user = user_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
) -> User:
    """
    Update an existing user.
    
    Args:
        user_id: User ID
        user_data: User update data
        db: Database session
        
    Returns:
        Updated user
        
    Raises:
        HTTPException: If user not found or email already exists
    """
    try:
        user_crud = get_user_crud(db)
        return user_crud.update(user_id, user_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a user.
    
    Args:
        user_id: User ID
        db: Database session
        
    Raises:
        HTTPException: If user not found
    """
    try:
        user_crud = get_user_crud(db)
        user_crud.delete(user_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )