from fastapi.testclient import TestClient


def test_create_valid_task(client: TestClient):
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "A description"},
    )
    assert response.status_code == 201
    payload = response.json()
    assert "data" in payload
    task = payload["data"]
    assert task["id"] == 1
    assert task["title"] == "Test Task"
    assert task["description"] == "A description"
    assert task["status"] == "pending"
    assert "created_at" in task
    assert "updated_at" in task


def test_create_empty_title_fails(client: TestClient):
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 400
    payload = response.json()
    assert "error" in payload
    assert payload["error"]["message"] == "Validation error"


def test_create_whitespace_only_title_fails(client: TestClient):
    response = client.post("/api/tasks", json={"title": "     "})
    assert response.status_code == 400
    payload = response.json()
    assert "error" in payload
    assert any(detail["field"] == "title" for detail in payload["error"]["details"])


def test_create_title_too_long_fails(client: TestClient):
    response = client.post("/api/tasks", json={"title": "x" * 256})
    assert response.status_code == 400
    payload = response.json()
    assert "error" in payload


def test_list_tasks_and_status_filter(client: TestClient):
    # Create two tasks
    client.post("/api/tasks", json={"title": "Pending Task"})
    created_second = client.post("/api/tasks", json={"title": "To Complete"}).json()["data"]
    client.patch(f"/api/tasks/{created_second['id']}/toggle")

    # List all
    res_all = client.get("/api/tasks")
    assert res_all.status_code == 200
    assert len(res_all.json()["data"]) == 2

    # Filter pending
    res_pending = client.get("/api/tasks?status=pending")
    assert res_pending.status_code == 200
    assert len(res_pending.json()["data"]) == 1
    assert res_pending.json()["data"][0]["status"] == "pending"

    # Filter completed
    res_completed = client.get("/api/tasks?status=completed")
    assert res_completed.status_code == 200
    assert len(res_completed.json()["data"]) == 1
    assert res_completed.json()["data"][0]["status"] == "completed"

    # Invalid status
    res_invalid = client.get("/api/tasks?status=bad_status")
    assert res_invalid.status_code == 400
    assert "Invalid status filter" in res_invalid.json()["error"]["message"]


def test_put_update_task(client: TestClient):
    created = client.post("/api/tasks", json={"title": "Original"}).json()["data"]
    task_id = created["id"]

    # Valid update
    res = client.put(f"/api/tasks/{task_id}", json={"title": "Updated", "description": "New desc"})
    assert res.status_code == 200
    assert res.json()["data"]["title"] == "Updated"
    assert res.json()["data"]["description"] == "New desc"

    # Unknown ID -> 404
    res_404 = client.put("/api/tasks/9999", json={"title": "Does not exist"})
    assert res_404.status_code == 404
    assert "not found" in res_404.json()["error"]["message"]

    # Invalid status in update -> 400
    res_bad_status = client.put(f"/api/tasks/{task_id}", json={"status": "invalid"})
    assert res_bad_status.status_code == 400


def test_patch_toggle_task(client: TestClient):
    created = client.post("/api/tasks", json={"title": "Toggle Me"}).json()["data"]
    task_id = created["id"]
    assert created["status"] == "pending"

    # Toggle to completed
    res1 = client.patch(f"/api/tasks/{task_id}/toggle")
    assert res1.status_code == 200
    assert res1.json()["data"]["status"] == "completed"

    # Toggle back to pending
    res2 = client.patch(f"/api/tasks/{task_id}/toggle")
    assert res2.status_code == 200
    assert res2.json()["data"]["status"] == "pending"

    # Toggle non-existent ID -> 404
    res_404 = client.patch("/api/tasks/9999/toggle")
    assert res_404.status_code == 404


def test_delete_task(client: TestClient):
    created = client.post("/api/tasks", json={"title": "Delete Me"}).json()["data"]
    task_id = created["id"]

    # Delete success
    res = client.delete(f"/api/tasks/{task_id}")
    assert res.status_code == 200
    assert res.json()["data"] == {"id": task_id}

    # Second delete returns 404
    res_repeat = client.delete(f"/api/tasks/{task_id}")
    assert res_repeat.status_code == 404


def test_non_integer_task_id_returns_400(client: TestClient):
    res = client.patch("/api/tasks/abc/toggle")
    assert res.status_code == 400
    assert res.json()["error"]["message"] == "Validation error"


def test_create_and_sort_by_priority(client: TestClient):
    client.post("/api/tasks", json={"title": "Low Priority Task", "priority": "low"})
    client.post("/api/tasks", json={"title": "High Priority Task", "priority": "high"})
    client.post("/api/tasks", json={"title": "Medium Priority Task", "priority": "medium"})

    res = client.get("/api/tasks")
    assert res.status_code == 200
    tasks = res.json()["data"]
    # High must come before Medium, which must come before Low
    priorities = [t["priority"] for t in tasks]
    assert priorities == ["high", "medium", "low"]


def test_invalid_priority_returns_400(client: TestClient):
    res = client.post("/api/tasks", json={"title": "Bad Priority", "priority": "urgent"})
    assert res.status_code == 400
    assert res.json()["error"]["message"] == "Validation error"


def test_task_with_due_date(client: TestClient):
    res = client.post(
        "/api/tasks",
        json={"title": "Task with date", "due_date": "2026-11-15", "priority": "high"},
    )
    assert res.status_code == 201
    task = res.json()["data"]
    assert task["due_date"] == "2026-11-15"
    assert task["priority"] == "high"

    # Invalid date format returns 400
    res_bad_date = client.post(
        "/api/tasks",
        json={"title": "Task with bad date", "due_date": "not-a-date"},
    )
    assert res_bad_date.status_code == 400
