from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Path, Query, status

from app.api.deps import get_task_service
from app.schemas.task import (
    TaskCreate,
    TaskDeleteResponse,
    TaskListResponse,
    TaskResponse,
    TaskUpdate,
)
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse, status_code=status.HTTP_200_OK)
def list_tasks(
    service: Annotated[TaskService, Depends(get_task_service)],
    status: Optional[str] = Query(None, description="Filter by status: pending or completed"),
) -> dict:
    """Retrieve all tasks, optionally filtered by status."""
    tasks = service.list_tasks(status=status)
    return {"data": tasks}


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    service: Annotated[TaskService, Depends(get_task_service)],
) -> dict:
    """Create a new task."""
    task = service.create_task(data=data)
    return {"data": task}


@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(
    task_id: Annotated[int, Path(..., description="The ID of the task to update")],
    data: TaskUpdate,
    service: Annotated[TaskService, Depends(get_task_service)],
) -> dict:
    """Update task fields (title, description, status)."""
    task = service.update_task(task_id=task_id, data=data)
    return {"data": task}


@router.patch("/{task_id}/toggle", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def toggle_task(
    task_id: Annotated[int, Path(..., description="The ID of the task to toggle")],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> dict:
    """Toggle task status between pending and completed."""
    task = service.toggle_task(task_id=task_id)
    return {"data": task}


@router.delete("/{task_id}", response_model=TaskDeleteResponse, status_code=status.HTTP_200_OK)
def delete_task(
    task_id: Annotated[int, Path(..., description="The ID of the task to delete")],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> dict:
    """Delete a task by ID."""
    service.delete_task(task_id=task_id)
    return {"data": {"id": task_id}}
