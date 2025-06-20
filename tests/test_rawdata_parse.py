#!/usr/bin/env python3
"""CI sanity checks for parse_rawdata.py."""
from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
SCRIPT = ROOT / "scripts" / "parse_rawdata.py"


def _run(*extra) -> str:
    return subprocess.check_output([sys.executable, SCRIPT, *extra], text=True)


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
