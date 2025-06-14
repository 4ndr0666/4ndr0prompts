#!/usr/bin/env python3
"""
promptlib_cli.py — Robust interactive CLI for promptlib.py using prompt_toolkit.
- Multi-select, validation, preview, and colorized status.
- Requires: prompt_toolkit (pip install prompt_toolkit), promptlib.py in same dir.
"""

import os
import sys
import datetime
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.shortcuts import radiolist_dialog, checkboxlist_dialog, input_dialog, message_dialog, yes_no_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import PathCompleter

# ---- Defensive promptlib import ----
try:
    import promptlib
except ImportError as e:
    print(f"\033[31mFATAL: Could not import promptlib.py: {e}\033[0m")
    sys.exit(1)

def get_category_choices():
    try:
        cats = list(getattr(promptlib, "TEMPLATES", {}).keys())
        return cats if cats else []
    except Exception:
        return []

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
    with open(output_path, "w") as f:
        f.write(f"# Category: {category}\n")
        f.write(f"# Generated: {timestamp}\n")
        f.write(f"# Prompt Count: {len(prompts)}\n\n")
        for idx, p in enumerate(prompts, 1):
            f.write(f"{idx}. {p}\n\n")
    # Also audit
    audit_dir = "prompt_logs"
    safe_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(audit_dir, exist_ok=True)
    with open(os.path.join(audit_dir, "prompt_audit.log"), "a") as log:
        for p in prompts:
            log.write(f"{safe_ts}\t{category}\t{p}\n")

style = Style.from_dict({
    'dialog':             'bg:#23272e #ffffff',
    'dialog.body':        'bg:#23272e #6ee7b7',
    'dialog shadow':      'bg:#23272e',
    'button':             'bg:#38bdf8 #222222',
    'button-arrow':       '#facc15',
    'dialog frame.label': 'bg:#38bdf8 #000000',
})

def main():
    categories = get_category_choices()
    if not categories:
        print("\033[31mFATAL: No prompt categories found in promptlib.py!\033[0m")
        sys.exit(1)
    # Multi-select (checkboxlist) dialog
    selected = checkboxlist_dialog(
        title="PromptLib Category Selection",
        text="Select one or more categories to generate prompts for:",
        values=[(cat, cat) for cat in categories],
        style=style
    ).run()
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
        validator=IntValidator()
    ).run()
    if not count:
        print("Aborted. No count entered.")
        sys.exit(0)
    count = int(count)
    # Config file (optional)
    config_path = input_dialog(
        title="Optional Config",
        text="Enter path to JSON config (optional):",
        completer=PathCompleter(expanduser=True, only_directories=False)
    ).run()
    if config_path:
        config_path = config_path.strip()
        if not is_valid_config(config_path):
            message_dialog(
                title="ERROR",
                text=f"Config file not found: {config_path}",
                style=style
            ).run()
            sys.exit(1)
    else:
        config_path = None

    # For each category: preview and save
    for idx, cat in enumerate(selected):
        try:
            templates, slots = promptlib.load_config(config_path)
            template = templates[cat]
            slotset = slots[cat]
            prompts = [promptlib.generate_prompt(template, slotset) for _ in range(count)]
        except Exception as e:
            message_dialog(
                title="ERROR",
                text=f"Failed to generate for {cat}:\n{e}",
                style=style
            ).run()
            continue
        # Preview dialog
        preview = "\n".join([f"{i+1}. {p}" for i, p in enumerate(prompts)])
        if not yes_no_dialog(
            title=f"Preview for '{cat}' ({idx+1}/{len(selected)})",
            text=f"{preview}\n\nSave these prompts?",
            style=style
        ).run():
            continue
        # Save
        outdir = ensure_output_dir(cat)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        outfile = f"{outdir}/prompts_{cat}_{ts}.txt"
        write_previewed_prompts(cat, prompts, outfile)
        message_dialog(
            title="Saved",
            text=f"Prompts saved to:\n{outfile}",
            style=style
        ).run()
    # Final message
    message_dialog(
        title="PromptLib CLI Done",
        text="Prompt generation complete.\nAudit: prompt_logs/prompt_audit.log",
        style=style
    ).run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)
