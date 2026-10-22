import os
import pytest
from datetime import date
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config

from app.models.task import Task
from app.repositories.task_repository import SqlTaskRepository
from app.schemas.task import TaskCreate, TaskUpdate

# 1. Read TEST_DATABASE_URL from environment or .env
TEST_DB_URL = os.getenv("TEST_DATABASE_URL")

# Check connectivity helper
def _is_db_reachable(url: str) -> bool:
    try:
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        return True
    except Exception:
        return False

# Skip the whole module if TEST_DATABASE_URL is not set or unreachable
if not TEST_DB_URL or not _is_db_reachable(TEST_DB_URL):
    pytestmark = pytest.mark.skip(
        reason="TEST_DATABASE_URL not set or target PostgreSQL database is unreachable"
    )
else:
    pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def db_engine():
    """Run alembic upgrade head once for the integration test module."""
    # Programmatically run alembic migrations on TEST_DATABASE_URL
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.upgrade(alembic_cfg, "head")

    engine = create_engine(TEST_DB_URL, pool_pre_ping=True)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    """Provide a fresh session and clean tasks table before and after each test."""
    TestingSession = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)
    session = TestingSession()

    # Clean tasks table
    session.execute(text("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE"))
    session.commit()

    yield session

    session.rollback()
    session.execute(text("TRUNCATE TABLE tasks RESTART IDENTITY CASCADE"))
    session.commit()
    session.close()


def test_sql_repository_crud_round_trip(db_session):
    repo = SqlTaskRepository(db=db_session)

    # 1. Create
    created = repo.create(
        TaskCreate(
            title="Postgres Integration Task",
            description="Testing real database",
            priority="high",
            due_date=date(2026, 12, 31),
        )
    )
    assert created.id is not None
    assert created.title == "Postgres Integration Task"
    assert created.priority == "high"
    assert created.status == "pending"

    # 2. Get
    fetched = repo.get(created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.due_date == date(2026, 12, 31)

    # 3. Update
    updated = repo.update(
        fetched,
        TaskUpdate(
            title="Updated Title in Postgres",
            status="completed",
            priority="low",
        ),
    )
    assert updated.title == "Updated Title in Postgres"
    assert updated.status == "completed"
    assert updated.priority == "low"

    # 4. Delete
    repo.delete(updated)
    assert repo.get(created.id) is None


def test_sql_repository_case_priority_ordering(db_session):
    repo = SqlTaskRepository(db=db_session)

    # Insert low, medium, high in random order
    repo.create(TaskCreate(title="Low Task", priority="low"))
    repo.create(TaskCreate(title="High Task 1", priority="high"))
    repo.create(TaskCreate(title="Medium Task", priority="medium"))
    repo.create(TaskCreate(title="High Task 2", priority="high"))

    tasks = repo.list()
    # Expect High Task 2, High Task 1, Medium Task, Low Task (CASE ordering + created_at DESC)
    priorities = [t.priority for t in tasks]
    assert priorities == ["high", "high", "medium", "low"]
    assert tasks[0].title == "High Task 2"
    assert tasks[1].title == "High Task 1"


def test_postgres_check_constraint_status_fails(db_session):
    """Directly insert an invalid status to prove PostgreSQL engine CHECK constraint fires."""
    with pytest.raises(IntegrityError):
        db_session.execute(
            text(
                "INSERT INTO tasks (title, status, priority, created_at, updated_at) "
                "VALUES ('Bad Status', 'invalid_status', 'medium', NOW(), NOW())"
            )
        )
        db_session.commit()


def test_postgres_check_constraint_priority_fails(db_session):
    """Directly insert an invalid priority to prove PostgreSQL engine CHECK constraint fires."""
    with pytest.raises(IntegrityError):
        db_session.execute(
            text(
                "INSERT INTO tasks (title, status, priority, created_at, updated_at) "
                "VALUES ('Bad Priority', 'pending', 'urgent', NOW(), NOW())"
            )
        )
        db_session.commit()
