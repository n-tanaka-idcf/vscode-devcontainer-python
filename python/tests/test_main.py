from types import ModuleType

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_app_is_fastapi_instance(api_main_module: ModuleType):
    assert hasattr(api_main_module, "app")
    assert isinstance(api_main_module.app, FastAPI)


def test_hello_endpoint_returns_expected_payload(client: TestClient):
    resp = client.get("/hello")
    assert resp.status_code == 200
    assert resp.headers.get("content-type", "").startswith("application/json")
    assert resp.json() == {"message": "hello world!"}


def test_hello_endpoint_method_not_allowed_for_post(client: TestClient):
    resp = client.post("/hello", json={})
    assert resp.status_code == 405
    body = resp.json()
    assert body["detail"] == "Method Not Allowed"


def test_unknown_path_returns_404(client: TestClient):
    resp = client.get("/does-not-exist")
    assert resp.status_code == 404
    body = resp.json()
    assert body["detail"] == "Not Found"


def test_openapi_contains_hello_path(client: TestClient):
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    data = resp.json()

    assert "paths" in data
    assert "/hello" in data["paths"]
    assert "get" in data["paths"]["/hello"]


def test_docs_endpoints_are_exposed_by_default(client: TestClient):
    # FastAPI が提供するインタラクティブな API ドキュメント UI を、このアプリでは
    # 「デフォルト URL（docs_url=/docs, redoc_url=/redoc）のまま公開する」ことを前提とした設計になっている。
    # 今後 docs_url / redoc_url をアプリ側で変更する場合、この仕様変更を検知するためにこのテストは失敗し、
    # それに合わせて期待するパスを更新する必要がある（ドキュメント UI を提供しない方針ならテストごと見直す）。
    docs = client.get("/docs")
    redoc = client.get("/redoc")

    assert docs.status_code == 200
    assert redoc.status_code == 200
    assert "text/html" in docs.headers.get("content-type", "")
    assert "text/html" in redoc.headers.get("content-type", "")
