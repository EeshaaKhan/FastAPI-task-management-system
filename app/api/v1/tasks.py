"""
app/api/v1/tasks/py
Task API endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.api.deps import get_db
from app.crud import get_task_crud
from app.models.task import TaskStatus
from app.schemas import Task, TaskCreate, TaskUpdate, TaskStatusUpdate
from app.utils.exceptions import NotFoundError

router = APIRouter()


@router.post("/users/{user_id}/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
) -> Task:
    """
    Create a new task for a user.
    
    Args:
        user_id: User ID
        task_data: Task creation data
        db: Database session
        
    Returns:
        Created task
        
    Raises:
        HTTPException: If user not found
    """
    try:
        task_crud = get_task_crud(db)
        return task_crud.create(task_data, user_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/users/{user_id}/tasks/", response_model=List[Task])
def get_user_tasks(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[TaskStatus] = None,
    db: Session = Depends(get_db)
) -> List[Task]:
    """
    Get all tasks for a user with optional status filtering.
    
    Args:
        user_id: User ID
        skip: Number of records to skip
        limit: Maximum number of records to return
        status_filter: Optional status filter
        db: Database session
        
    Returns:
        List of tasks
    """
    task_crud = get_task_crud(db)
    
    if status_filter:
        return task_crud.get_by_status(user_id, status_filter)
    else:
        return task_crud.get_by_user_id(user_id, skip=skip, limit=limit)


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
) -> Task:
    """
    Get task by ID.
    
    Args:
        task_id: Task ID
        db: Database session
        
    Returns:
        Task data
        
    Raises:
        HTTPException: If task not found
    """
    task_crud = get_task_crud(db)
    task = task_crud.get_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
) -> Task:
    """
    Update an existing task.
    
    Args:
        task_id: Task ID
        task_data: Task update data
        db: Database session
        
    Returns:
        Updated task
        
    Raises:
        HTTPException: If task not found
    """
    try:
        task_crud = get_task_crud(db)
        return task_crud.update(task_id, task_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/tasks/{task_id}/status", response_model=Task)
def update_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    db: Session = Depends(get_db)
) -> Task:
    """
    Update task status.
    
    Args:
        task_id: Task ID
        status_data: Status update data
        db: Database session
        
    Returns:
        Updated task
        
    Raises:
        HTTPException: If task not found
    """
    try:
        task_crud = get_task_crud(db)
        return task_crud.update_status(task_id, status_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a task.
    
    Args:
        task_id: Task ID
        db: Database session
        
    Raises:
        HTTPException: If task not found
    """
    try:
        task_crud = get_task_crud(db)
        task_crud.delete(task_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/users/{user_id}/tasks/stats")
def get_user_task_stats(
    user_id: int,
    db: Session = Depends(get_db)
) -> dict:
    """
    Get task statistics for a user.
    
    Args:
        user_id: User ID
        db: Database session
        
    Returns:
        Task statistics
    """
    task_crud = get_task_crud(db)
    
    total_tasks = task_crud.count_by_user(user_id)
    todo_tasks = task_crud.count_by_status(user_id, TaskStatus.TODO)
    in_progress_tasks = task_crud.count_by_status(user_id, TaskStatus.IN_PROGRESS)
    done_tasks = task_crud.count_by_status(user_id, TaskStatus.DONE)
    
    return {
        "user_id": user_id,
        "total_tasks": total_tasks,
        "todo_tasks": todo_tasks,
        "in_progress_tasks": in_progress_tasks,
        "done_tasks": done_tasks,
        "completion_rate": round((done_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
    }