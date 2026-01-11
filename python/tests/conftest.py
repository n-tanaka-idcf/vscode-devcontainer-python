import importlib.util
from pathlib import Path
import sys
from types import ModuleType

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


# `pytest` エントリポイント（.venv/bin/pytest）から起動した場合、sys.path[0] が
# .venv/bin になりプロジェクトルートが import パスに入らないことがある。
# `from api...` を安定させるため、テスト開始時にルートを明示的に追加する。
_root = str(_project_root())
if _root not in sys.path:
    sys.path.insert(0, _root)


def _api_main_path() -> Path:
    return _project_root() / "api" / "main.py"


def _load_api_main_module() -> ModuleType:
    # パッケージ構成（api/__init__.py の有無）に依存せずにテストできるように、パス指定で読み込む
    # これにより、プロジェクトのパッケージ化の段階や実行コンテキスト（pytest の実行場所など）が変わっても、同じテストコードで安定して api/main.py を検証できるようにしている
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
