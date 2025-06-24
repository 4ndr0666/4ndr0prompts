#!/usr/bin/env python3
"""promptlib2.py — dataset-based prompt retrieval library.

This module loads NSFW prompts from ``dataset/templates.json`` via the
canonical loader in :mod:`prompt_config`. It provides a small API for
generating prompts and listing categories/slots.  Legacy parsing of the
``nsfwprompts.txt`` corpus has been removed in favour of the canonical
JSON configuration.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import Iterable, List, Dict, Tuple

import prompt_config

DEFAULT_CATEGORY = "other_uncategorized"


@dataclass
class PromptEntry:
    category: str
    prompt: str
    tags: List[str]
    original_id: str = ""
    source_hash: str = ""


def _load() -> Tuple[Dict[str, str], Dict[str, Dict[str, List[str]]]]:
    """Load templates and slots using :func:`prompt_config.load_config`."""
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        _CONFIG_CACHE = prompt_config.load_config()
    return _CONFIG_CACHE


_CONFIG_CACHE: Tuple[Dict[str, str], Dict[str, Dict[str, List[str]]]] | None = None


def load_prompts() -> List[PromptEntry]:
    """Generate one prompt per category using the canonical templates."""
    templates, slots = _load()
    entries: List[PromptEntry] = []
    for cat, template in templates.items():
        slotset = slots.get(cat, {})
        prompt = prompt_config.generate_prompt(template, slotset)
        entries.append(PromptEntry(category=cat, prompt=prompt, tags=[cat]))
    return entries


def get_categories() -> List[str]:
    """Return all available categories."""
    templates, _ = _load()
    return sorted(templates.keys())


def get_slots(category: str) -> Dict[str, List[str]]:
    """Return slot mapping for ``category`` or raise ``KeyError``."""
    _, slots = _load()
    if category not in slots:
        raise KeyError(category)
    return slots[category]


def list_categories(prompts: Iterable[PromptEntry] | None = None) -> List[str]:
    """Return sorted categories from prompts."""
    if prompts is not None:
        return sorted({p.category for p in prompts})
    return get_categories()


def get_random_prompts(
    count: int = 1, category: str | None = None
) -> List[PromptEntry]:
    """Return a list of random ``PromptEntry`` objects."""
    templates, slots = _load()
    categories = [category] if category else list(templates.keys())
    if category and category not in templates:
        return []
    entries: List[PromptEntry] = []
    for _ in range(count):
        cat = random.choice(categories)
        template = templates[cat]
        slotset = slots.get(cat, {})
        prompt = prompt_config.generate_prompt(template, slotset)
        entries.append(PromptEntry(category=cat, prompt=prompt, tags=[cat]))
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Dataset prompt generator")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--count", type=int, default=5, help="Number of prompts")
    parser.add_argument("--output", type=str, default="", help="Output file")
    parser.add_argument("--dry-run", action="store_true", help="Do not write file")
    args = parser.parse_args()

    prompts = get_random_prompts(args.count, args.category)
    if not prompts:
        print("No prompts found for the given options.")
        return

    lines = [p.prompt for p in prompts]
    output = "\n".join(lines)
    if args.output and not args.dry_run:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output + "\n")
    print(output)


if __name__ == "__main__":
    main()
