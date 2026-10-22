import pytest
from app.core.errors import NotFoundError, ValidationError
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from tests.conftest import FakeTaskRepository


def test_service_create_and_get():
    repo = FakeTaskRepository()
    service = TaskService(repository=repo)

    task = service.create_task(TaskCreate(title="Test Task", description="Details"))
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.status == "pending"

    fetched = service.get_task(task.id)
    assert fetched.id == 1


def test_service_get_not_found():
    repo = FakeTaskRepository()
    service = TaskService(repository=repo)

    with pytest.raises(NotFoundError) as exc_info:
        service.get_task(999)
    assert "999 not found" in exc_info.value.message


def test_service_toggle_flips_status():
    repo = FakeTaskRepository()
    service = TaskService(repository=repo)

    task = service.create_task(TaskCreate(title="Toggle test"))
    assert task.status == "pending"

    toggled = service.toggle_task(task.id)
    assert toggled.status == "completed"

    toggled_again = service.toggle_task(task.id)
    assert toggled_again.status == "pending"


def test_service_update_and_delete():
    repo = FakeTaskRepository()
    service = TaskService(repository=repo)

    task = service.create_task(TaskCreate(title="To be updated"))
    updated = service.update_task(task.id, TaskUpdate(title="Updated Title"))
    assert updated.title == "Updated Title"

    service.delete_task(task.id)
    with pytest.raises(NotFoundError):
        service.get_task(task.id)


def test_service_list_with_invalid_status_filter():
    repo = FakeTaskRepository()
    service = TaskService(repository=repo)

    with pytest.raises(ValidationError) as exc_info:
        service.list_tasks(status="invalid_filter")
    assert "Invalid status filter" in exc_info.value.message
