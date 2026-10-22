from typing import List, Optional

from app.core.errors import NotFoundError, ValidationError
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate

VALID_STATUSES = {"pending", "completed"}


class TaskService:
    """Business logic service for managing tasks. Depends on TaskRepository protocol (DIP)."""

    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        if status is not None:
            normalized_status = status.strip().lower()
            if normalized_status not in VALID_STATUSES:
                raise ValidationError(
                    message=f"Invalid status filter '{status}'. Must be 'pending' or 'completed'."
                )
            status = normalized_status
        return self.repository.list(status=status)

    def get_task(self, task_id: int) -> Task:
        task = self.repository.get(task_id=task_id)
        if task is None:
            raise NotFoundError(message=f"Task with id {task_id} not found")
        return task

    def create_task(self, data: TaskCreate) -> Task:
        return self.repository.create(data=data)

    def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        task = self.get_task(task_id=task_id)
        return self.repository.update(task=task, data=data)

    def toggle_task(self, task_id: int) -> Task:
        task = self.get_task(task_id=task_id)
        new_status = "completed" if task.status == "pending" else "pending"
        update_data = TaskUpdate(status=new_status)
        return self.repository.update(task=task, data=update_data)

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id=task_id)
        self.repository.delete(task=task)
