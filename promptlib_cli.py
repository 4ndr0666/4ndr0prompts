#!/usr/bin/env python3
"""
promptlib_cli.py — Robust interactive CLI for promptlib.py using prompt_toolkit.
- Multi-select, validation, preview, and colorized status.
- Requires: prompt_toolkit (pip install prompt_toolkit), promptlib.py in same dir.
"""

import os
import sys
import datetime
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.shortcuts import (
    input_dialog,
    message_dialog,
    yes_no_dialog,
)
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import PathCompleter
from prompt_config import generate_prompt, load_config

DEFAULT_LOG_DIR = os.path.join(
    os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share")),
    "redteam-prompts",
    "logs",
)


_DATA_CACHE: tuple[dict, dict] | None = None


def load_data(config_path: str | None = None) -> tuple[dict, dict]:
    """Return templates and slots from configuration with caching."""
    global _DATA_CACHE
    if _DATA_CACHE is None or config_path is not None:
        if config_path is None:
            _DATA_CACHE = load_config()
        else:
            _DATA_CACHE = load_config(config_path)
    return _DATA_CACHE


def get_category_choices(config_path: str | None = None) -> list[str]:
    """Return category keys from the dataset configuration."""
    try:
        templates, _ = load_data(config_path)
        return list(templates.keys())
    except Exception:
        return []


def _slot_preview(category: str, slots: dict[str, dict[str, list]]) -> str:
    slotmap = slots.get(category, {})
    lines = []
    for slot, values in slotmap.items():
        sample = ", ".join(values[:2])
        lines.append(f"{slot}: {sample}")
    return "\n".join(lines) if lines else "No slots available."


def select_categories(
    categories: list[str], slots: dict[str, dict[str, list]]
) -> list[str]:
    """Interactively select categories using fuzzy completion with slot preview."""
    completer = FuzzyWordCompleter(categories, WORD=True)
    selected: list[str] = []
    while True:
        choice = prompt(
            "Category (ENTER to finish): ",
            completer=completer,
            style=style,
        ).strip()
        if not choice:
            break
        if choice in categories and choice not in selected:
            preview = _slot_preview(choice, slots)
            if yes_no_dialog(
                title=f"Add '{choice}'?",
                text=f"{preview}\n\nAdd this category?",
                style=style,
            ).run():
                selected.append(choice)
        else:
            message_dialog(
                title="ERROR",
                text=f"Unknown category: {choice}",
                style=style,
            ).run()
    return selected


def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def is_valid_config(config_path):
    return not config_path or os.path.isfile(config_path)


def ensure_output_dir(category):
    outdir = f"prompts_out/{category}"
    os.makedirs(outdir, exist_ok=True)
    return outdir


def write_previewed_prompts(category, prompts, output_path):
    timestamp = now_str()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Category: {category}\n")
        f.write(f"# Generated: {timestamp}\n")
        f.write(f"# Prompt Count: {len(prompts)}\n\n")
        for idx, p in enumerate(prompts, 1):
            f.write(f"{idx}. {p}\n\n")
    # Also audit
    audit_dir = DEFAULT_LOG_DIR
    safe_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(audit_dir, exist_ok=True)
    with open(
        os.path.join(audit_dir, "prompt_audit.log"), "a", encoding="utf-8"
    ) as log:
        for p in prompts:
            log.write(f"{safe_ts}\t{category}\t{p}\n")


style = Style.from_dict(
    {
        "dialog": "bg:#23272e #ffffff",
        "dialog.body": "bg:#23272e #6ee7b7",
        "dialog shadow": "bg:#23272e",
        "button": "bg:#38bdf8 #222222",
        "button-arrow": "#facc15",
        "dialog frame.label": "bg:#38bdf8 #000000",
    }
)


def main():
    categories = get_category_choices()
    if not categories:
        print("\033[31mFATAL: No prompt categories found in promptlib.py!\033[0m")
        sys.exit(1)
    message_dialog(
        title="PromptLib Category Selection",
        text="Enter categories (press ENTER on blank line to finish).",
        style=style,
    ).run()
    _, slots_data = load_data()
    selected = select_categories(categories, slots_data)
    if not selected:
        print("Aborted. No categories selected.")
        sys.exit(0)

    # Prompt count (validated)
    class IntValidator(Validator):
        def validate(self, doc):
            try:
                v = int(doc.text)
                if not (1 <= v <= 1000):
                    raise ValueError
            except Exception:
                raise ValidationError(message="Enter a number 1-1000")

    count = input_dialog(
        title="Prompt Count",
        text="Enter prompt count per category (1-1000):",
        validator=IntValidator(),
    ).run()
    if not count:
        print("Aborted. No count entered.")
        sys.exit(0)
    count = int(count)
    # Config file (optional)
    config_path = input_dialog(
        title="Optional Config",
        text="Enter path to JSON config (optional):",
        completer=PathCompleter(expanduser=True, only_directories=False),
    ).run()
    if config_path:
        config_path = config_path.strip()
        if not is_valid_config(config_path):
            message_dialog(
                title="ERROR", text=f"Config file not found: {config_path}", style=style
            ).run()
            sys.exit(1)
    else:
        config_path = None

    # For each category: preview and save
    for idx, cat in enumerate(selected):
        try:
            templates, slots = load_config(config_path)
            template = templates[cat]
            slotset = slots[cat]
        except Exception as e:
            message_dialog(
                title="ERROR", text=f"Failed to load data for {cat}:\n{e}", style=style
            ).run()
            continue

        while True:
            prompts = [generate_prompt(template, slotset) for _ in range(count)]
            preview = "\n".join([f"{i+1}. {p}" for i, p in enumerate(prompts)])
            if yes_no_dialog(
                title=f"Preview for '{cat}' ({idx+1}/{len(selected)})",
                text=f"{preview}\n\nSave these prompts? (No = regenerate)",
                style=style,
            ).run():
                outdir = ensure_output_dir(cat)
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                outfile = f"{outdir}/prompts_{cat}_{ts}.txt"
                write_previewed_prompts(cat, prompts, outfile)
                message_dialog(
                    title="Saved", text=f"Prompts saved to:\n{outfile}", style=style
                ).run()
                break
    # Final message
    message_dialog(
        title="PromptLib CLI Done",
        text=(
            "Prompt generation complete.\nAudit: " f"{DEFAULT_LOG_DIR}/prompt_audit.log"
        ),
        style=style,
    ).run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)
