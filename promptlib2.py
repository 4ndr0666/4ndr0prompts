#!/usr/bin/env python3
"""promptlib2.py — dataset-based prompt retrieval library.

This module loads NSFW prompts from the dataset directory and provides
an interface similar to ``promptlib.py``. Prompts are categorized using
simple keyword heuristics for filtering.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import random
import re
from dataclasses import dataclass
from typing import Iterable, List

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset", "nsfwprompts.txt")
DEFAULT_CATEGORY = "other_uncategorized"

# Mapping from dataset slugs to template keys.
# Keep this in sync with ``dataset/templates.json`` to ensure category names
# remain stable across libraries.
CATEGORY_MAP = {
    "mention_of_removing_cloths_garments_dress_and_revealing_chest": "clothing_chest_exposure",
    "mentions_of_turning_around_revealing_butt": "turning_bending_buttocks",
    "mention_of_inserting_an_object_or_anything_into_mouth": "insertion_oral_mouth",
    "mention_of_multiple_people": "multi_person_interaction",
    "if_not_in_any_categories_above_yet_mention_of_white_fluid_liquid": "white_fluid_dripping",
    "everything_else_left_over": "other_uncategorized",
}


@dataclass
class PromptEntry:
    category: str
    prompt: str
    tags: List[str]
    original_id: str
    source_hash: str


def _clean_line(text: str) -> str:
    """Return cleaned prompt text or an empty string if invalid."""
    cleaned = text.strip()
    if not cleaned or cleaned.startswith(("###", "---")):
        return ""
    cleaned = re.sub(r"^Prompt\s*\d+:\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^\d+\.\s*", "", cleaned)
    return cleaned.strip()


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def parse_dataset(path: str = DATASET_PATH) -> List[tuple[int, str, str]]:
    """Parse dataset file into ``(line_no, category, text)`` tuples."""
    prompts: List[tuple[int, str, str]] = []
    current_category = DEFAULT_CATEGORY
    with open(path, "r", encoding="utf-8") as fh:
        for idx, line in enumerate(fh, 1):
            stripped = line.strip()
            if stripped.startswith("### Verification"):
                break
            m = re.match(r"###\s*Category\s*\d+:(.*)", stripped)
            if m:
                slug = _slugify(m.group(1))
                current_category = CATEGORY_MAP.get(slug, slug) or DEFAULT_CATEGORY
                continue
            cleaned = _clean_line(stripped)
            if cleaned:
                prompts.append((idx, current_category, cleaned))
    return prompts


def aggregate_prompts(path: str = DATASET_PATH) -> List[PromptEntry]:
    """Aggregate prompts with metadata from the dataset."""
    prompts = parse_dataset(path)
    entries: List[PromptEntry] = []
    seen = set()
    for line_no, category, text in prompts:
        if text in seen:
            continue
        seen.add(text)
        source_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        entries.append(
            PromptEntry(
                category=category,
                prompt=text,
                tags=[category],
                original_id=f"{os.path.basename(path)}:line_{line_no}",
                source_hash=source_hash,
            )
        )
    return entries


_PROMPTS_CACHE: List[PromptEntry] | None = None


def load_prompts(path: str = DATASET_PATH) -> List[PromptEntry]:
    """Load prompts from dataset with caching."""
    global _PROMPTS_CACHE
    if _PROMPTS_CACHE is None:
        _PROMPTS_CACHE = aggregate_prompts(path)
    return list(_PROMPTS_CACHE)


def list_categories(prompts: Iterable[PromptEntry] | None = None) -> List[str]:
    """Return sorted categories from prompts."""
    data = list(prompts) if prompts else load_prompts()
    return sorted({p.category for p in data})


def get_random_prompts(
    count: int = 1, category: str | None = None
) -> List[PromptEntry]:
    """Return a list of random ``PromptEntry`` objects."""
    data = load_prompts()
    if category:
        data = [p for p in data if p.category == category]
    if not data:
        return []
    return random.sample(data, k=min(count, len(data)))


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

