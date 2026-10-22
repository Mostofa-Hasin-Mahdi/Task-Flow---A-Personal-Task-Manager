from typing import List, Optional, Protocol
from sqlalchemy import desc, select
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
        stmt = stmt.order_by(desc(Task.created_at))
        return list(self.db.scalars(stmt).all())

    def get(self, task_id: int) -> Optional[Task]:
        stmt = select(Task).where(Task.id == task_id)
        return self.db.scalars(stmt).first()

    def create(self, data: TaskCreate) -> Task:
        task = Task(
            title=data.title,
            description=data.description,
            status="pending",
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

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
