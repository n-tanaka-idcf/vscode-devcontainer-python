from fastapi.testclient import TestClient


def test_list_tasks_returns_expected_shape(client: TestClient):
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.headers.get("content-type", "").startswith("application/json")

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1

    task = data[0]
    assert task["id"] == 1
    assert task["title"] == "1つ目のToDoタスク"
    assert task["done"] is False


def test_create_task_accepts_title_and_returns_id(client: TestClient):
    resp = client.post("/tasks", json={"title": "牛乳を買う"})
    assert resp.status_code == 200
    assert resp.json() == {"id": 1, "title": "牛乳を買う"}


def test_create_task_allows_empty_body_and_returns_null_title(client: TestClient):
    resp = client.post("/tasks", json={})
    assert resp.status_code == 200
    assert resp.json() == {"id": 1, "title": None}


def test_create_task_requires_json_body(client: TestClient):
    # body 自体がない場合は validation error になる（TaskCreate が required）
    resp = client.post("/tasks")
    assert resp.status_code == 422


def test_update_task_returns_path_id(client: TestClient):
    resp = client.put("/tasks/123", json={"title": "更新後"})
    assert resp.status_code == 200
    assert resp.json() == {"id": 123, "title": "更新後"}


def test_update_task_requires_int_task_id(client: TestClient):
    resp = client.put("/tasks/not-an-int", json={"title": "x"})
    assert resp.status_code == 422


def test_update_task_requires_json_body(client: TestClient):
    resp = client.put("/tasks/1")
    assert resp.status_code == 422


def test_delete_task_returns_success(client: TestClient):
    resp = client.delete("/tasks/1")
    assert resp.status_code == 200
    # FastAPI は None を JSON null として返すことが多いが、将来変更にも耐えるように緩めに確認する
    assert resp.content in (b"null", b"", None)


def test_delete_task_requires_int_task_id(client: TestClient):
    resp = client.delete("/tasks/not-an-int")
    assert resp.status_code == 422


def test_method_not_allowed_for_tasks_collection(client: TestClient):
    resp = client.put("/tasks", json={"title": "x"})
    assert resp.status_code == 405


def test_method_not_allowed_for_task_item_get(client: TestClient):
    resp = client.get("/tasks/1")
    assert resp.status_code == 405
