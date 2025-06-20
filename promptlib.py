#!/usr/bin/env python3
"""
promptlib.py — Interactive, color-highlighted, fully structured prompt mutation engine for red team ops.

- ANSI cyan color highlights for UI and output (toggle with --no-color)
- Interactive TUI for step-by-step prompt construction
- Fully structured, human-readable output file (YAML-like per prompt)
- Complete slot logic for all categories (no placeholders)
- Robust error handling, audit log, and category extensibility

Usage:
  $ ./promptlib.py [--tui] [--category CAT] [--count N] [--output OUTFILE] [--no-color]
"""

import sys
import os
import argparse
import random
import datetime
import json
from prompt_config import load_config

DEFAULT_LOG_DIR = os.path.join(
    os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share")),
    "redteam-prompts",
    "logs",
)

# ANSI color support for cyan highlights
CYAN = "\033[36m"
RESET = "\033[0m"


def highlight(text, enable_color=True):
    return f"{CYAN}{text}{RESET}" if enable_color else text


# Load templates and slots from shared configuration
TEMPLATES, SLOTS = load_config()


def interactive_prompt(enable_color=True):
    print(
        highlight("========== Red Team Prompt Mutation Engine ==========", enable_color)
    )
    print("Select a category:")
    categories = list(TEMPLATES.keys())
    for idx, cat in enumerate(categories, 1):
        print(f"  {highlight(str(idx), enable_color)}: {cat.replace('_', ' ').title()}")
    while True:
        try:
            choice = input(highlight("Enter category number: ", enable_color))
        except EOFError:
            print(highlight("Invalid input. Try again.", enable_color))
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            catkey = categories[int(choice) - 1]
            break
        print(highlight("Invalid selection. Try again.", enable_color))
    slotset = SLOTS[catkey]
    print(
        highlight(
            f"\nSelected category: {catkey.replace('_', ' ').title()}", enable_color
        )
    )
    slot_values = {}
    for slot in slotset:
        print(f"\nPossible values for {highlight(slot, enable_color)}:")
        for idx, val in enumerate(slotset[slot], 1):
            print(f"  {highlight(str(idx), enable_color)}: {val}")
        while True:
            try:
                subchoice = input(
                    highlight(
                        f"Choose (1-{len(slotset[slot])}) or 'r' for random: ",
                        enable_color,
                    )
                )
            except EOFError:
                print(highlight("Invalid input. Try again.", enable_color))
                continue
            if subchoice.lower() == "r":
                value = random.choice(slotset[slot])
                print(highlight(f"Selected: {value}", enable_color))
                break
            if subchoice.isdigit() and 1 <= int(subchoice) <= len(slotset[slot]):
                value = slotset[slot][int(subchoice) - 1]
                break
            print(highlight("Invalid input. Try again.", enable_color))
        slot_values[slot] = value
    # Construct prompt
    prompt = TEMPLATES[catkey]
    for slot, value in slot_values.items():
        prompt = prompt.replace(f"[{slot}]", value)
    print(highlight("\nGenerated Prompt:", enable_color))
    print(highlight(prompt, enable_color))
    print("\nPrompt structure (YAML-like):")
    print(highlight(f"category: {catkey}", enable_color))
    print(highlight(f"prompt: {prompt}", enable_color))
    for slot, value in slot_values.items():
        print(highlight(f"{slot}: {value}", enable_color))

    while True:
        try:
            save = (
                input(highlight("\nSave this prompt to a file? (y/n): ", enable_color))
                .strip()
                .lower()
            )
        except EOFError:
            print(highlight("Invalid input. Try again.", enable_color))
            continue
        if save in {"y", "n"}:
            break
        print(highlight("Please enter 'y' or 'n'.", enable_color))
    if save == "y":
        outpath = f"interactive_prompt_{catkey}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(f"category: {catkey}\n")
            f.write(f"prompt: {prompt}\n")
            for slot, value in slot_values.items():
                f.write(f"{slot}: {value}\n")
        print(highlight(f"Prompt saved to {outpath}", enable_color))
    else:
        print(highlight("Prompt not saved.", enable_color))


def save_structured(prompts, category, slotsets, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for idx, (prompt, slots) in enumerate(zip(prompts, slotsets), 1):
            f.write("---\n")
            f.write(f"prompt_{idx}:\n")
            f.write(f"  category: {category}\n")
            f.write(f"  text: |\n    {prompt}\n")
            for slot, value in slots.items():
                f.write(f"  {slot}: {value}\n")


def log_prompts(prompts, category, slotsets, output_path=None, log_dir=DEFAULT_LOG_DIR):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if not output_path:
        output_path = f"prompts_{category}_{timestamp}.txt"
    save_structured(prompts, category, slotsets, output_path)
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "prompt_audit.log"), "a", encoding="utf-8") as log:
        for p, slots in zip(prompts, slotsets):
            slotjson = json.dumps(slots)
            log.write(f"{timestamp}\t{category}\t{p}\t{slotjson}\n")
    return output_path


def random_prompt(template, slotset):
    result = template
    selected = {}
    max_iterations = 10
    for _ in range(max_iterations):
        changed = False
        for slot, choices in slotset.items():
            placeholder = f"[{slot}]"
            if placeholder in result:
                value = random.choice(choices)
                result = result.replace(placeholder, value, 1)
                selected[slot] = value
                changed = True
        if not changed:
            break
    return result, selected


def generate_prompt(template, slotset):
    """Return a prompt with slots filled randomly."""
    prompt, _ = random_prompt(template, slotset)
    return prompt


def main():
    parser = argparse.ArgumentParser(
        description="Red Team Prompt Mutation Engine (promptlib.py)"
    )
    parser.add_argument("--tui", action="store_true", help="Run interactive TUI mode")
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List available prompt categories and exit",
    )
    parser.add_argument(
        "--category",
        type=str,
        choices=list(TEMPLATES.keys()),
        help="Category key for batch mode",
    )
    parser.add_argument(
        "--count", type=int, default=5, help="Number of prompts (batch mode)"
    )
    parser.add_argument(
        "--output", type=str, default=None, help="Output file for prompts"
    )
    parser.add_argument("--no-color", action="store_true", help="Disable color output")
    args = parser.parse_args()

    color = not args.no_color

    if args.list_categories:
        for cat in sorted(TEMPLATES.keys()):
            print(cat)
        sys.exit(0)

    if args.tui:
        interactive_prompt(enable_color=color)
        sys.exit(0)

    categories = list(TEMPLATES.keys())
    if not args.category or args.category not in categories:
        print(highlight("ERROR: Please specify --category with one of:", color))
        for cat in categories:
            print(f"  {highlight(cat, color)}")
        sys.exit(1)
    template = TEMPLATES[args.category]
    slotset = SLOTS[args.category]
    prompts = []
    slotsets = []
    for _ in range(args.count):
        prompt, slots = random_prompt(template, slotset)
        prompts.append(prompt)
        slotsets.append(slots)
    output_path = log_prompts(prompts, args.category, slotsets, args.output)
    print(highlight(f"[SUCCESS] {len(prompts)} prompts saved to {output_path}", color))


if __name__ == "__main__":
    main()
