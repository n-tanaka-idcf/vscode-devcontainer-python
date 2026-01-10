import importlib.util
from pathlib import Path
from types import ModuleType

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _api_main_path() -> Path:
    return _project_root() / "api" / "main.py"


def _load_api_main_module() -> ModuleType:
    # パッケージ構成（api/__init__.py の有無）に依存せずにテストできるように、パス指定で読み込む
    spec = importlib.util.spec_from_file_location(
        "api_main_test_module", _api_main_path()
    )
    assert spec is not None and spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def api_main_module() -> ModuleType:
    return _load_api_main_module()


@pytest.fixture()
def client(api_main_module: ModuleType) -> TestClient:
    assert hasattr(api_main_module, "app"), (
        "api/main.py に FastAPI インスタンス `app` が定義されている必要があります"
    )
    app = api_main_module.app
    assert isinstance(app, FastAPI)
    return TestClient(app)


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
    # FastAPI のデフォルト設定（docs_url=/docs, redoc_url=/redoc）を前提にしたスモークテスト
    docs = client.get("/docs")
    redoc = client.get("/redoc")

    assert docs.status_code == 200
    assert redoc.status_code == 200
    assert "text/html" in docs.headers.get("content-type", "")
    assert "text/html" in redoc.headers.get("content-type", "")
