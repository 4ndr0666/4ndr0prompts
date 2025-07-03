#!/usr/bin/env python3
"""Canonical loader providing hot reload of dataset and plugins.

This module centralises all option sourcing per CODEX/AGENTS.
It loads templates and slots via ``prompt_config`` and merges
plugin options via ``plugin_loader``. Results are cached and
reloaded when source files change.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple
import json

import prompt_config
import plugin_loader

_CACHE: dict[tuple[str, str], tuple[float, float, Tuple[dict, dict, dict]]] = {}
_OPTS_CACHE: dict[str, Tuple[float, dict]] = {}


def _mtimes(config: Path, plugin_dir: Path) -> tuple[float, float]:
    cfg_mtime = config.stat().st_mtime if config.exists() else 0.0
    plugin_mtime = 0.0
    if plugin_dir.is_dir():
        for p in plugin_dir.iterdir():
            try:
                plugin_mtime = max(plugin_mtime, p.stat().st_mtime)
            except FileNotFoundError:
                continue
    return cfg_mtime, plugin_mtime


def load_canonical(
    config_path: str | None = None, plugin_dir: str | None = None
) -> tuple[dict, dict, dict]:
    """Return templates, slots, and plugin options with hot reload."""
    cfg_path = Path(config_path or prompt_config.CONFIG_PATH)
    plug_path = Path(plugin_dir or "plugins")
    mtime = _mtimes(cfg_path, plug_path)
    cache_key = (str(cfg_path), str(plug_path))
    cached = _CACHE.get(cache_key)
    if cached and cached[0:2] == mtime:
        return cached[2]

    templates, slots = prompt_config.load_config(str(cfg_path))
    plugins: Dict[str, list] = {}
    if plug_path.is_dir():
        plugins = plugin_loader.load_plugin_dir(plug_path)
    _CACHE[cache_key] = (*mtime, (templates, slots, plugins))
    return templates, slots, plugins


def is_valid_option(category: str, option: str, plugins: dict) -> bool:
    """Return True if option is valid for category."""
    opts = plugins.get(category, [])
    return option in opts


def load_options(path: str | None = None) -> dict:
    """Load base option lists from dataset with hot reload."""
    opt_path = Path(path or Path(__file__).parent / "dataset" / "options.json")
    mtime = opt_path.stat().st_mtime if opt_path.exists() else 0.0
    cached = _OPTS_CACHE.get(str(opt_path))
    if cached and cached[0] == mtime:
        return cached[1]
    if not opt_path.is_file():
        _OPTS_CACHE[str(opt_path)] = (mtime, {})
        return {}
    data = json.loads(opt_path.read_text(encoding="utf-8"))
    _OPTS_CACHE[str(opt_path)] = (mtime, data)
    return data
