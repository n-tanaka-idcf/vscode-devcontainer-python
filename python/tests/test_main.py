import importlib.util
import runpy
import subprocess
import sys
from pathlib import Path

EXPECTED_STDOUT = "Hello from python!\n"


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _main_path() -> Path:
    return _project_root() / "main.py"


def _normalize_newlines(s: str) -> str:
    return s.replace("\r\n", "\n")


def test_main_function_prints_expected_message(capsys):
    import main

    ret = main.main()
    captured = capsys.readouterr()

    assert ret is None
    assert captured.out == EXPECTED_STDOUT
    assert captured.err == ""


def test_main_symbol_is_callable():
    import main

    assert hasattr(main, "main")
    assert callable(main.main)


def test_importing_module_does_not_print_anything(capsys):
    # __name__ != "__main__" で読み込まれる限り、トップレベル実行は発生しないことを確認
    spec = importlib.util.spec_from_file_location("main_import_test", _main_path())
    assert spec is not None and spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_running_as_script_prints_expected_message(capsys):
    # if __name__ == "__main__": が期待通り動作することを確認
    runpy.run_module("main", run_name="__main__")
    captured = capsys.readouterr()

    assert captured.out == EXPECTED_STDOUT
    assert captured.err == ""


def test_running_via_python_m_main_prints_expected_message():
    result = subprocess.run(
        [sys.executable, "-m", "main"],
        cwd=_project_root(),
        capture_output=True,
        text=True,
        check=True,
    )

    assert _normalize_newlines(result.stdout) == EXPECTED_STDOUT
    assert result.stderr == ""


def test_running_via_python_main_py_prints_expected_message():
    result = subprocess.run(
        [sys.executable, str(_main_path())],
        cwd=_project_root(),
        capture_output=True,
        text=True,
        check=True,
    )

    assert _normalize_newlines(result.stdout) == EXPECTED_STDOUT
    assert result.stderr == ""
