#!/usr/bin/env python3
"""Shared configuration loader for templates and slots."""

from __future__ import annotations

import json
import os
import random
from typing import Dict

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "dataset", "templates.json")

_templates: Dict[str, str] | None = None
_slots: Dict[str, Dict[str, list]] | None = None


def load_config(
    path: str = CONFIG_PATH,
) -> tuple[Dict[str, str], Dict[str, Dict[str, list]]]:
    """Load templates and slots from JSON configuration."""
    global _templates, _slots
    if _templates is None or _slots is None:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        _templates = data.get("templates", {})
        _slots = data.get("slots", {})
    return _templates, _slots


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

