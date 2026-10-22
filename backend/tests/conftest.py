from datetime import date, datetime, timezone
from typing import Generator, List, Optional
import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_task_service
from app.main import app
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService

PRIORITY_RANK = {"high": 1, "medium": 2, "low": 3}


class FakeTaskRepository(TaskRepository):
    """In-memory task repository implementing the TaskRepository Protocol (LSP & DIP)."""

    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self._next_id: int = 1

    def list(self, status: Optional[str] = None) -> List[Task]:
        results = [t for t in self.tasks if status is None or t.status == status]
        # Sort by priority (high first), then created_at descending
        return sorted(
            results,
            key=lambda t: (PRIORITY_RANK.get(t.priority, 4), -t.created_at.timestamp()),
        )

    def get(self, task_id: int) -> Optional[Task]:
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def create(self, data: TaskCreate) -> Task:
        now = datetime.now(timezone.utc)
        task = Task(
            id=self._next_id,
            title=data.title,
            description=data.description,
            status="pending",
            priority=data.priority or "medium",
            due_date=data.due_date,
            created_at=now,
            updated_at=now,
        )
        self._next_id += 1
        self.tasks.append(task)
        return task

    def update(self, task: Task, data: TaskUpdate) -> Task:
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.status is not None:
            task.status = data.status
        if data.priority is not None:
            task.priority = data.priority
        if data.due_date is not None:
            task.due_date = data.due_date
        task.updated_at = datetime.now(timezone.utc)
        return task

    def delete(self, task: Task) -> None:
        self.tasks = [t for t in self.tasks if t.id != task.id]


@pytest.fixture
def fake_repo() -> FakeTaskRepository:
    """Fixture providing a fresh in-memory repository for each test."""
    return FakeTaskRepository()


@pytest.fixture
def task_service(fake_repo: FakeTaskRepository) -> TaskService:
    """Fixture providing a TaskService instance backed by FakeTaskRepository."""
    return TaskService(repository=fake_repo)


@pytest.fixture
def client(task_service: TaskService) -> Generator[TestClient, None, None]:
    """TestClient fixture overriding get_task_service dependency with in-memory service."""
    app.dependency_overrides[get_task_service] = lambda: task_service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
