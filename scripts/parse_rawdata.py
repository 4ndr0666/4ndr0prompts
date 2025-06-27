#!/usr/bin/env python3
"""Parse raw dataset and generate templates and slot reports."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from typing import Dict, Iterable, List

RAWDATA_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "rawdata.txt")
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")

CATEGORY_RULES = {
    "turning_bending_buttocks": re.compile(r"buttocks|culo|rear", re.I),
    "clothing_chest_exposure": re.compile(r"breast|chest|areola", re.I),
    "insertion_oral_mouth": re.compile(r"mouth|suck|oral", re.I),
    "multi_person_interaction": re.compile(
        r"kiss|touch|caress|stroke|hold|embrace", re.I
    ),
    "white_fluid_dripping": re.compile(r"fluid|liquid|esperma|yfluid", re.I),
}
DEFAULT_CATEGORY = "other_uncategorized"

SLOT_PATTERNS: Dict[str, Dict[str, re.Pattern[str]]] = {
    "turning_bending_buttocks": {
        "CLOTHING_BOTTOM": re.compile(r"skirt|pants|trunks|leggings?|tanga", re.I),
        "BUTTOCKS_DESC": re.compile(
            r"round buttocks|bare buttocks|bottom|backside|thighs", re.I
        ),
    },
    "clothing_chest_exposure": {
        "ACTION": re.compile(r"drool|smack|lean|dance|jiggle|sway|grope", re.I),
    },
    "white_fluid_dripping": {
        "LIQUID_DESC": re.compile(r"pearly|milky|viscous|ropey|stringy|yfluid", re.I),
    },
    "multi_person_interaction": {
        "INTERACTION": re.compile(
            r"kiss(?:es)?|touch|caress|stroke|hold|embrace", re.I
        ),
    },
}


def _read_raw(path: str) -> List[str]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)


def needs_update(raw_path: str, output_dir: str) -> bool:
    """Return True if outputs are missing or older than raw data."""
    out_json = os.path.join(output_dir, "templates.json")
    report = os.path.join(output_dir, "slots_report.tsv")
    if not os.path.exists(out_json) or not os.path.exists(report):
        return True
    raw_mtime = os.path.getmtime(raw_path)
    return raw_mtime > os.path.getmtime(out_json) or raw_mtime > os.path.getmtime(
        report
    )


def _categorize(text: str) -> str:
    for cat, pattern in CATEGORY_RULES.items():
        if pattern.search(text):
            return cat
    return DEFAULT_CATEGORY


def _extract_slots(text: str, category: str) -> Dict[str, List[str]]:
    slots: Dict[str, List[str]] = {}
    patterns = SLOT_PATTERNS.get(category, {})
    for name, pattern in patterns.items():
        values = sorted({m.group(0).strip() for m in pattern.finditer(text)})
        if values:
            slots[name] = values
    return slots


def parse_lines(lines: Iterable[str], trim_sentences: int = 1):
    templates: Dict[str, str] = {}
    slots: Dict[str, Dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for line in lines:
        category = _categorize(line)
        first_sent = ".".join(line.split(".")[:trim_sentences]).strip()
        templates.setdefault(category, first_sent)
        slot_values = _extract_slots(line, category)
        for slot, vals in slot_values.items():
            slots[category][slot].update(vals)
    # convert sets to sorted lists
    final_slots = {
        cat: {s: sorted(list(vals)) for s, vals in sd.items()}
        for cat, sd in slots.items()
    }
    for cat in CATEGORY_RULES:
        final_slots.setdefault(cat, {})
        templates.setdefault(cat, templates.get(cat, ""))
    final_slots.setdefault(DEFAULT_CATEGORY, {})
    templates.setdefault(DEFAULT_CATEGORY, templates.get(DEFAULT_CATEGORY, ""))
    return templates, final_slots


def write_outputs(
    templates: Dict[str, str], slots: Dict[str, Dict[str, List[str]]], output_dir: str
) -> None:
    os.makedirs(output_dir, exist_ok=True)
    out_json = os.path.join(output_dir, "templates.json")
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump({"templates": templates, "slots": slots}, fh, indent=2)
    report = os.path.join(output_dir, "slots_report.tsv")
    with open(report, "w", encoding="utf-8") as fh:
        for cat, slot_map in slots.items():
            for slot, values in slot_map.items():
                for val in values:
                    val = val.replace("\t", "\\t").replace("\n", " ")
                    fh.write(f"{cat}\t{slot}\t{val}\n")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse raw dataset")
    parser.add_argument(
        "--force", action="store_true", help="Rewrite outputs even if up-to-date"
    )
    parser.add_argument(
        "--trim-sentences",
        type=int,
        default=1,
        help="Number of sentences to keep for templates",
    )
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)

    lines = _read_raw(RAWDATA_PATH)
    templates, slots = parse_lines(lines, args.trim_sentences)
    if args.force or needs_update(RAWDATA_PATH, args.output_dir):
        write_outputs(templates, slots, args.output_dir)
    else:
        print("Outputs up to date", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
