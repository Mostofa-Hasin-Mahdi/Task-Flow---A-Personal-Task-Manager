from typing import List, Optional, Protocol
from sqlalchemy import case, desc, select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository(Protocol):
    """Protocol defining the task repository interface (Interface Segregation / Dependency Inversion)."""

    def list(self, status: Optional[str] = None) -> List[Task]:
        ...

    def get(self, task_id: int) -> Optional[Task]:
        ...

    def create(self, data: TaskCreate) -> Task:
        ...

    def update(self, task: Task, data: TaskUpdate) -> Task:
        ...

    def delete(self, task: Task) -> None:
        ...


class SqlTaskRepository:
    """SQLAlchemy 2.0 implementation of TaskRepository. The ONLY place that touches the DB session."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, status: Optional[str] = None) -> List[Task]:
        stmt = select(Task)
        if status is not None:
            stmt = stmt.where(Task.status == status)

        # Sort by priority (high=1, medium=2, low=3) using CASE, then created_at descending
        priority_order = case(
            (Task.priority == "high", 1),
            (Task.priority == "medium", 2),
            (Task.priority == "low", 3),
            else_=4,
        )
        stmt = stmt.order_by(priority_order, desc(Task.created_at))
        return list(self.db.scalars(stmt).all())

    def get(self, task_id: int) -> Optional[Task]:
        stmt = select(Task).where(Task.id == task_id)
        return self.db.scalars(stmt).first()

    def create(self, data: TaskCreate) -> Task:
        task = Task(
            title=data.title,
            description=data.description,
            status="pending",
            priority=data.priority or "medium",
            due_date=data.due_date,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
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

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
