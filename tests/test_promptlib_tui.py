import importlib
import sys

import pytest


def test_importable(monkeypatch):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    try:
        module = importlib.import_module("promptlib_tui")
    except ModuleNotFoundError as exc:
        pytest.skip(str(exc))
    assert module
