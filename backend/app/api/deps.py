from typing import Annotated, Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.task_repository import SqlTaskRepository
from app.services.task_service import TaskService


def get_task_service(db: Annotated[Session, Depends(get_db)]) -> TaskService:
    """Dependency provider wiring SqlTaskRepository to TaskService."""
    repository = SqlTaskRepository(db=db)
    return TaskService(repository=repository)


__all__ = ["get_db", "get_task_service", "Depends"]
