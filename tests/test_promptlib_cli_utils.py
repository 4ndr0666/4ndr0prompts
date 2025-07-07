from pathlib import Path

import promptlib_cli as cli


def test_get_category_choices():
    cats = cli.get_category_choices()
    templates, _ = cli.load_data()
    assert set(cats) == set(templates.keys())


def test_slot_preview_contains_slot():
    cfg = cli.load_dict()
    text = cli._slot_preview("insertion_oral_mouth", cfg)
    assert "object" in text.lower()


def test_ensure_output_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    out = cli.ensure_output_dir("example")
    assert Path(out).is_dir()
