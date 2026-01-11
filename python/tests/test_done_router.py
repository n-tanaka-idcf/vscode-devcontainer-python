from fastapi.testclient import TestClient


def test_mark_task_as_done_returns_success(client: TestClient):
    resp = client.put("/tasks/1/done")
    assert resp.status_code == 200
    assert resp.content in (b"null", b"", None)


def test_unmark_task_as_done_returns_success(client: TestClient):
    resp = client.delete("/tasks/1/done")
    assert resp.status_code == 200
    assert resp.content in (b"null", b"", None)


def test_done_endpoints_require_int_task_id(client: TestClient):
    resp_put = client.put("/tasks/not-an-int/done")
    resp_delete = client.delete("/tasks/not-an-int/done")

    assert resp_put.status_code == 422
    assert resp_delete.status_code == 422


def test_method_not_allowed_for_done_get(client: TestClient):
    resp = client.get("/tasks/1/done")
    assert resp.status_code == 405
