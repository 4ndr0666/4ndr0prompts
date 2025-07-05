#!/usr/bin/env python3
"""CLI for inspecting canonical prompt data.

This tool relies on ``canonical_loader`` per CODEX and AGENTS
to ensure all options come from the canonical chain.
"""
from __future__ import annotations

import argparse
import sys

from canonical_loader import list_categories, list_slots


def main() -> None:
    parser = argparse.ArgumentParser(description="Canonical dataset inspector")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--list-categories",
        action="store_true",
        help="List available prompt categories",
    )
    group.add_argument(
        "--show-slots",
        metavar="CATEGORY",
        help="Show slots for the given category",
    )
    args = parser.parse_args()

    if args.list_categories:
        for cat in list_categories():
            print(cat)
        return

    slots = list_slots(args.show_slots)
    if not slots:
        print(f"Unknown category: {args.show_slots}", file=sys.stderr)
        sys.exit(1)
    for slot, values in slots.items():
        joined = ", ".join(values)
        print(f"{slot}: {joined}")


if __name__ == "__main__":
    main()
