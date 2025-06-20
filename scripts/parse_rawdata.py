#!/usr/bin/env python3
"""Canonicalise rawdata.txt into templates.json. Dry-run unless --write."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Final

DATASET_ENV = os.environ.get("DATASET_DIR")

ROOT: Final = Path(__file__).resolve().parents[1]
DATASET: Final = Path(DATASET_ENV).resolve() if DATASET_ENV else ROOT / "dataset"
RAW: Final = DATASET / "rawdata.txt"
TJSON: Final = DATASET / "templates.json"
REPORT: Final = DATASET / "slots_report.tsv"

# Regex heuristics for category tagging (ordered, first-match wins)
CATEGORY_RULES: list[tuple[str, re.Pattern]] = [
    ("insertion_oral_mouth", re.compile(r"\b(suck|mouth|tongue|blow)\b", re.I)),
    (
        "clothing_chest_exposure",
        re.compile(r"\b(breast|brest|bosom|areola|grope|jiggle|sway)\b", re.I),
    ),
    (
        "turning_bending_buttocks",
        re.compile(
            r"\b(butt|glúteos|tanga|bottom|skirt|pants|trunks|leggings?)\b", re.I
        ),
    ),
    (
        "multi_person_interaction",
        re.compile(
            r"\b(two|2|manhoods|kiss(?:es)?|touch|caress|stroke|embrace|hold)\b", re.I
        ),
    ),
    (
        "white_fluid_dripping",
        re.compile(
            r"\b(pearly|milky|viscous|ropey|stringy|yfluid|esperma|fluid)\b", re.I
        ),
    ),
]
DEFAULT_CAT: Final = "other_uncategorized"

# 2.  Slot tokens we care about per category
SLOT_PATTERNS: dict[str, dict[str, re.Pattern]] = {
    "clothing_chest_exposure": {
        "CLOTHING_TOP": re.compile(
            r"(?:top garment|blouse|shirt|dress|article of clothing)", re.I
        ),
        "SKIN_DETAIL": re.compile(
            r"(blushing areolas|smooth skin|freckled skin|oiled)", re.I
        ),
        "ACTION": re.compile(r"(drool|smack|lean|dance|jiggle|sway|grope)", re.I),
    },
    "turning_bending_buttocks": {
        "CLOTHING_BOTTOM": re.compile(r"(skirt|pants|trunks|leggings?|tanga)", re.I),
        "BUTTOCKS_DESC": re.compile(
            r"(round buttocks|bare buttocks|bottom|backside|thighs)", re.I
        ),
        "BODY_MARKING": re.compile(r"(tattoo[^,.\n]*)", re.I),
    },
    "insertion_oral_mouth": {
        "OBJECT": re.compile(r"(black object|wiener|dick|tube|cylinder)", re.I),
        "LIQUID_DESC": re.compile(r"(viscous liquid|milky|yfluid|saliva)", re.I),
        "EYE_CONTACT": re.compile(r"(eye contact|stare|looking at the camera)", re.I),
    },
    "white_fluid_dripping": {
        "LIQUID_DESC": re.compile(r"(pearly|milky|viscous|ropey|stringy|yfluid)", re.I),
    },
    "multi_person_interaction": {
        "INTERACTION": re.compile(
            r"(kiss(?:es)?|touch|caress|stroke|hold|embrace)", re.I
        ),
    },
    # … extend as needed
}

Prompt = dict[str, str]  # {"text": str, "category": str}


def _read_raw() -> list[str]:
    """Return non-empty lines from RAW, exit if missing."""
    try:
        text = RAW.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"error: missing {RAW}", file=sys.stderr)
        raise SystemExit(1)
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def _classify(txt: str) -> str:
    for cat, pat in CATEGORY_RULES:
        if pat.search(txt):
            return cat
    return DEFAULT_CAT


def _extract_slots(category: str, txt: str) -> dict[str, set[str]]:
    slots: dict[str, set[str]] = defaultdict(set)
    for slot, pat in SLOT_PATTERNS.get(category, {}).items():
        for m in pat.finditer(txt):
            slots[slot].add(m.group(0).lower())
    return slots


def _trim_sentences(text: str, count: int) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    if parts and re.fullmatch(r"\d+\.", parts[0]) and len(parts) > 1:
        parts[0:2] = [f"{parts[0]} {parts[1]}"]
    return " ".join(parts[:count]).strip()


def parse(
    trim_sentences: int = 1,
) -> tuple[dict[str, str], dict[str, dict[str, list[str]]]]:
    templates: dict[str, str] = {}
    slots: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))

    for paragraph in _read_raw():
        cat = _classify(paragraph)
        if cat not in templates:
            templates[cat] = _trim_sentences(paragraph, trim_sentences)

        for slot, values in _extract_slots(cat, paragraph).items():
            slots[cat][slot].update(values)

    for cat in templates:
        slots.setdefault(cat, {})

    templates = dict(sorted(templates.items()))
    slots = {k: {s: sorted(v) for s, v in sv.items()} for k, sv in slots.items()}
    return templates, slots


def _write_output(
    templates: dict[str, str], slots: dict[str, dict[str, list[str]]]
) -> None:
    DATASET.mkdir(exist_ok=True)
    payload = {"templates": templates, "slots": slots}
    TJSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    with REPORT.open("w", encoding="utf-8") as fh:
        for cat, slotmap in slots.items():
            for slot, vals in slotmap.items():
                for v in vals:
                    safe = v.replace("\t", "\\t").replace("\n", " ")
                    fh.write(f"{cat}\t{slot}\t{safe}\n")


def main() -> None:
    p = argparse.ArgumentParser(
        description="Canonicalise rawdata.txt into templates.json"
    )
    p.add_argument("--write", action="store_true", help="Write output files")
    p.add_argument(
        "--trim-sentences",
        type=int,
        default=1,
        metavar="N",
        help="Keep first N sentences as template",
    )
    args = p.parse_args()

    templates, slots = parse(args.trim_sentences)
    payload = {"templates": templates, "slots": slots}

    if args.write:
        _write_output(templates, slots)
        target = TJSON if TJSON.is_absolute() else TJSON.resolve()
        print(f"[OK] wrote {target} and slots_report.tsv")
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
