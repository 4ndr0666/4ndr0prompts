#!/usr/bin/env python3
"""Shared configuration loader for templates and slots."""

from __future__ import annotations

import json
import os
import random
from typing import Dict

_CACHE: dict[str, tuple[Dict[str, str], Dict[str, Dict[str, list]]]] = {}

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "dataset", "templates.json")


def load_config(
    path: str = CONFIG_PATH,
) -> tuple[Dict[str, str], Dict[str, Dict[str, list]]]:
    """Load templates and slots from JSON configuration.

    Results are cached per absolute path to avoid repeated file reads.
    """
    abspath = os.path.abspath(path)
    if abspath not in _CACHE:
        with open(abspath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        templates = data.get("templates", {})
        slots = data.get("slots", {})
        _CACHE[abspath] = (templates, slots)
    return _CACHE[abspath]


def generate_prompt(template: str, slots: Dict[str, list]) -> str:
    """Return a prompt with placeholders replaced by random slot values."""
    result = template
    max_iterations = 10
    for _ in range(max_iterations):
        changed = False
        for slot, choices in slots.items():
            placeholder = f"[{slot}]"
            if placeholder in result:
                result = result.replace(placeholder, random.choice(choices), 1)
                changed = True
        if not changed:
            break
    return result
