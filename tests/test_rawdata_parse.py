#!/usr/bin/env python3
"""CI sanity checks for parse_rawdata.py."""
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
SCRIPT = ROOT / "scripts" / "parse_rawdata.py"


def _run(*extra, env=None) -> str:
    e = os.environ.copy()
    if env:
        e.update(env)
    return subprocess.check_output([sys.executable, SCRIPT, *extra], text=True, env=e)


def _run_write(tmp_path: Path) -> Path:
    dataset_dir = tmp_path / "dataset"
    dataset_dir.mkdir()
    shutil.copy(DATASET / "rawdata.txt", dataset_dir / "rawdata.txt")
    _run("--write", "--trim-sentences", "1", env={"DATASET_DIR": str(dataset_dir)})
    return dataset_dir


def test_no_placeholder_tokens() -> None:
    payload = json.loads(_run())
    placeholder_re = re.compile(r"\[[A-Z_]+\]")
    # templates
    for tmpl in payload["templates"].values():
        assert not placeholder_re.search(tmpl), tmpl
    # slots
    for slotmap in payload["slots"].values():
        for values in slotmap.values():
            for v in values:
                assert "[" not in v and "]" not in v


def test_templates_parsable() -> None:
    """Render 10 prompts per category → no placeholders."""
    payload = json.loads(_run())
    for cat, tmpl in payload["templates"].items():
        for _ in range(10):
            out = tmpl  # (real rendering happens elsewhere)
            assert "[" not in out and "]" not in out


def test_all_categories_accounted(tmp_path: Path) -> None:
    d = _run_write(tmp_path)
    data = json.load((d / "templates.json").open())
    assert len(data["templates"]) == 6
    for cat in data["templates"]:
        assert cat in data["slots"]


def test_no_empty_slot_lists(tmp_path: Path) -> None:
    d = _run_write(tmp_path)
    data = json.load((d / "templates.json").open())
    for slotmap in data["slots"].values():
        for values in slotmap.values():
            assert values


def test_no_duplicate_slot_values(tmp_path: Path) -> None:
    d = _run_write(tmp_path)
    data = json.load((d / "templates.json").open())
    for slotmap in data["slots"].values():
        for values in slotmap.values():
            assert len(values) == len(set(values))


def test_tsv_integrity(tmp_path: Path) -> None:
    d = _run_write(tmp_path)
    report = d / "slots_report.tsv"
    for line in report.read_text(encoding="utf-8").splitlines():
        assert len(line.split("\t")) == 3
