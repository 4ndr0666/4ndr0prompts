#!/usr/bin/env python3
"""
promptlib_tui.py — Error-hardened, robust TUI for promptlib.py red team prompt mutation.
Requirements: npyscreen (pip install npyscreen), promptlib.py in same directory.
"""

import sys
import os

# ---- TTY Safety Check ----
if not sys.stdin.isatty() or not sys.stdout.isatty():
    print("ERROR: promptlib_tui.py requires a real terminal (tty).")
    print("Run this script in a terminal window, not via backgrounded script or pipe.")
    sys.exit(1)

import npyscreen
import datetime

# ==== Defensive Import and Category Check ====
try:
    import promptlib
except ImportError:
    npyscreen.wrapper_basic(
        lambda: npyscreen.notify_confirm(
            "Could not import promptlib.py in the current directory.",
            title="FATAL: ImportError",
            wide=True,
        )
    )
    sys.exit(1)
    sys.exit(1)


def get_category_choices():
    # Always check for TEMPLATES
    try:
        cats = list(getattr(promptlib, "TEMPLATES", {}).keys())
        return cats if cats else []
    except Exception:
        return []


if not get_category_choices():
    npyscreen.wrapper_basic(
        lambda: npyscreen.notify_confirm(
            "No prompt categories found in promptlib.py (TEMPLATES is empty).\n"
            "Please check that promptlib.py is correct and present.",
            title="FATAL: No Categories",
            wide=True,
        )
    )
    sys.exit(1)


# ==== Utility Functions ====
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


# ==== Main TUI Classes ====
class PromptBatchForm(npyscreen.ActionForm):
    def create(self):
        categories = get_category_choices()
        if not categories:
            npyscreen.notify_confirm(
                "No prompt categories available! Check your promptlib.py.",
                title="FATAL: No Categories",
                wide=True,
            )
            self.parentApp.setNextForm(None)
            return
        self.categories = self.add(
            npyscreen.TitleMultiSelect,
            name="Categories (space to select multiple):",
            values=categories,
            scroll_exit=True,
            max_height=min(10, len(categories) + 2),
        )
        self.number = self.add(
            npyscreen.TitleText, name="Prompt Count per Category", value="5"
        )
        self.config = self.add(
            npyscreen.TitleFilenameCombo, name="Optional Config Path", value=""
        )

    def on_ok(self):
        try:
            chosen_indices = self.categories.value
            if not chosen_indices or not isinstance(chosen_indices, list):
                npyscreen.notify_confirm(
                    "Please select at least one category.",
                    title="Input Error",
                    wide=True,
                )
                return
            cats = get_category_choices()
            chosen_categories = [cats[i] for i in chosen_indices if 0 <= i < len(cats)]
            number = int(self.number.value.strip())
            config_path = self.config.value.strip() or None
            if not chosen_categories:
                npyscreen.notify_confirm(
                    "Please select at least one category.",
                    title="Input Error",
                    wide=True,
                )
                return
            if number < 1 or number > 1000:
                npyscreen.notify_confirm(
                    "Prompt count must be between 1 and 1000.",
                    title="Input Error",
                    wide=True,
                )
                return
            if not is_valid_config(config_path):
                npyscreen.notify_confirm(
                    "Config path is invalid or file does not exist.",
                    title="Input Error",
                    wide=True,
                )
                return
        except Exception as e:
            npyscreen.notify_confirm(
                f"Input Error: {e}", title="Input Error", wide=True
            )
            return
        self.parentApp.chosen_categories = chosen_categories
        self.parentApp.prompt_count = number
        self.parentApp.config_path = config_path
        self.parentApp.setNextForm("PREVIEW")

    def on_cancel(self):
        self.parentApp.setNextForm(None)


class PromptPreviewForm(npyscreen.ActionForm):
    def create(self):
        self.category_idx = 0
        self.add_handlers({"^Q": self.exit_form})
        self.title = self.add(npyscreen.FixedText, value="", editable=False, relx=2)
        self.preview_box = self.add(
            npyscreen.BoxTitle, name="Preview Prompts", max_height=16, rely=2
        )
        self.add(
            npyscreen.FixedText,
            value="Press OK to save these prompts and continue, or Cancel to skip this category.",
            editable=False,
            relx=2,
            rely=19,
        )

    def beforeEditing(self):
        cats = self.parentApp.chosen_categories
        self.category_idx = getattr(self, "category_idx", 0)
        self.cur_category = cats[self.category_idx]
        self.title.value = (
            f"Category: {self.cur_category} ({self.category_idx+1} of {len(cats)})"
        )
        # Generate prompts for preview
        try:
            templates, slots = promptlib.load_config(self.parentApp.config_path)
            template = templates[self.cur_category]
            slotset = slots[self.cur_category]
            self.prompts = [
                promptlib.generate_prompt(template, slotset)
                for _ in range(self.parentApp.prompt_count)
            ]
        except Exception as e:
            self.prompts = [f"[ERROR] {e}"]
        # Show preview
        self.preview_box.values = [
            f"{idx+1}. {p}" for idx, p in enumerate(self.prompts)
        ]

    def on_ok(self):
        outdir = ensure_output_dir(self.cur_category)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        outfile = f"{outdir}/prompts_{self.cur_category}_{ts}.txt"
        write_previewed_prompts(self.cur_category, self.prompts, outfile)
        npyscreen.notify_confirm(
            f"Prompts saved to: {outfile}\n\n(Next category will be shown, if any remain)",
            title="Saved",
            wide=True,
        )
        # Move to next category or exit
        if self.category_idx + 1 < len(self.parentApp.chosen_categories):
            self.category_idx += 1
            self.beforeEditing()
            self.display()
        else:
            self.parentApp.setNextForm("RESULT")

    def on_cancel(self):
        # Skip to next category or exit
        if self.category_idx + 1 < len(self.parentApp.chosen_categories):
            self.category_idx += 1
            self.beforeEditing()
            self.display()
        else:
            self.parentApp.setNextForm("RESULT")

    def exit_form(self, *args, **keywords):
        self.parentApp.setNextForm(None)
        self.editing = False


class ResultForm(npyscreen.FormBaseNew):
    def create(self):
        self.message = self.add(
            npyscreen.FixedText,
            value="Prompt generation complete.",
            editable=False,
            relx=2,
        )
        self.add(
            npyscreen.FixedText,
            value="Audit logs in prompt_logs/prompt_audit.log",
            editable=False,
            relx=2,
            rely=3,
        )
        self.add(
            npyscreen.FixedText,
            value="Press ENTER or ESC to exit.",
            editable=False,
            relx=2,
            rely=5,
        )


class PromptGenApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.chosen_categories = []
        self.prompt_count = 5
        self.config_path = ""
        self.addForm("MAIN", PromptBatchForm, name="PromptLib Red Team TUI")
        self.addForm("PREVIEW", PromptPreviewForm, name="Prompt Preview & Save")
        self.addForm("RESULT", ResultForm, name="Generation Complete")


def safe_cli_menu():
    cats = list(promptlib.TEMPLATES.keys())
    print("Choose a category:")
    for idx, cat in enumerate(cats):
        print(f"{idx+1}. {cat}")
    i = int(input("Enter number: ")) - 1
    n = int(input("Prompt count: "))
    for _ in range(n):
        print(
            promptlib.generate_prompt(
                promptlib.TEMPLATES[cats[i]], promptlib.SLOTS[cats[i]]
            )
        )


if __name__ == "__main__":
    safe_cli_menu()
    PromptGenApp().run()
