"""Prompt generation utilities."""

# SPDX-License-Identifier: MIT

from typing import Dict


def generate_prompt(template: str, slots: Dict[str, str]) -> str:
    """Return template formatted with slot values."""
    return template.format(**slots)
