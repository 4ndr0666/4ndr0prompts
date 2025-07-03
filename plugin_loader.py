#!/usr/bin/env python3
"""Plugin loader for canonical prompt options.

Loads plugin packs from a directory and normalises them into
``{category: [options...]}`` mappings. Supported formats are JSON, YAML and
Markdown code blocks. Unknown categories are placed into ``uncategorized``.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List

try:
    import yaml
except Exception as exc:  # pragma: no cover - yaml should always import
    raise RuntimeError("PyYAML required for plugin_loader") from exc

ALLOWED_CATEGORIES: set[str] = {
    "pose",
    "lighting",
    "lens",
    "camera_move",
    "environment",
    "shadow",
    "detail",
    "uncategorized",
}


class PluginLoaderError(Exception):
    pass


def _normalise_category(cat: str) -> str:
    cat = str(cat).lower().replace("-", "_").replace(" ", "_")
    return cat if cat in ALLOWED_CATEGORIES else "uncategorized"


def _parse_data(data: dict) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for cat, items in data.items():
        ncat = _normalise_category(cat)
        if ncat not in out:
            out[ncat] = []
        out[ncat].extend([str(i).strip() for i in list(items)])
    return out


def _parse_markdown(text: str) -> Dict[str, List[str]]:
    blocks = re.findall(r"```(?:\s*(json|yaml))?\n(.*?)\n```", text, re.DOTALL)
    merged: Dict[str, List[str]] = {}
    for lang, body in blocks:
        if lang and lang.strip() == "json":
            data = json.loads(body)
        else:
            data = yaml.safe_load(body)
        d = _parse_data(data or {})
        for k, vals in d.items():
            merged.setdefault(k, []).extend(vals)
    return merged


def _load_file(path: Path) -> Dict[str, List[str]]:
    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(text)
        return _parse_data(data)
    if suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
        return _parse_data(data or {})
    if suffix in {".md", ".markdown"}:
        return _parse_markdown(text)
    raise PluginLoaderError(f"Unsupported plugin format: {path}")


def load_plugin_dir(directory: str | Path) -> Dict[str, List[str]]:
    """Load plugins from directory, returning categorized options."""
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise PluginLoaderError(f"Plugin directory not found: {dir_path}")

    merged: Dict[str, List[str]] = {}
    allowed_suffixes = {".json", ".yaml", ".yml", ".md", ".markdown"}
    for path in dir_path.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in allowed_suffixes:
            continue
        data = _load_file(path)
        for cat, items in data.items():
            merged.setdefault(cat, []).extend(items)

    for cat in list(merged):
        deduped = sorted({item for item in merged[cat] if item})
        merged[cat] = deduped
    return merged
