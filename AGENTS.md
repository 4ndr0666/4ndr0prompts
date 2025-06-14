# AGENTS.md — Red-Team Prompt Mutation Toolkit
# Repository Root: <repo>/        (branch: main)
#
# Purpose
# ───────
# This repository houses the *Red-Team Prompt Mutation Toolkit* — a Python-centric
# library plus CLI/TUI front-ends for generating adversarial prompts that probe
# NSFW filter boundaries.  It is distinct from any cinematic/Sora prompt libs.
#
# Directory Summary
# ─────────────────
# .
# ├── category1…category6/    # slot-lists & category templates (Python)
# ├── promptlib_redteam.py    # ★ unified core generator  ← primary import
# ├── promptlib_cli.py        # prompt-toolkit interface  (console-script: promptlib-rt)
# ├── promptlib_tui.py        # npyscreen TUI             (console-script: promptlib-rt-tui)
# ├── promptlib.py            # Cinematic library (independent; do not mutate)
# ├── promptlib_redteam/plugins/   # YAML / MD plug-ins (Prompts1 corpus lives here)
# ├── scripts/                # helper utilities (import_prompts1.py, gen_catalogue.py)
# ├── var/                    # runtime artefacts — logs & generated batches  ➜ git-ignored
# ├── tests/                  # pytest suite (≥ 85 % coverage target)
# ├── docs/                   # slot-catalogue & developer docs
# ├── codex-merge-clean.sh    # merge-artifact scrubber (must run pre-commit)
# ├── pre-commit              # hook invoking shellcheck, shfmt, ruff, pytest
# └── pyproject.toml          # PEP 621 build metadata  (editable install)
#
# Canonical Workflow
# ──────────────────
#   git checkout -b feature/<task>
#   ./codex-merge-clean.sh $(git ls-files '*.sh' '*.py')
#   ruff --fix . && black .
#   pytest -q && pytest --cov=promptlib_redteam -q
#   git add -u && git commit -m "<type>: <message>"
#   pre-commit run --all-files
#
# Coding & Lint Standards
# ───────────────────────
# * Python 3.10+, PEP 8 via **ruff** auto-fix + **black** (88 cols).
# * Shell scripts: POSIX-sh, `set -euo pipefail`, pass **shellcheck** & **shfmt**.
# * Always implement `--help` & `--dry-run` in scripts affecting filesystem.
# * Log-files under `$XDG_DATA_HOME/redteam/logs/` or `var/prompt_logs/`.
# * No placeholders / truncated logic (see CODEX.md for merge policy).
# * Execute `codex-merge-clean.sh` on every changed file pre-commit.
#
# XDG Compliance
# ──────────────
#   CONFIG ➜   ${XDG_CONFIG_HOME:-$HOME/.config}/redteam-prompts/
#   DATA   ➜   ${XDG_DATA_HOME:-$HOME/.local/share}/redteam-prompts/
#   CACHE  ➜   ${XDG_CACHE_HOME:-$HOME/.cache}/redteam-prompts/
#
# Required Tests (minimum)
# ────────────────────────
# 1. Slot-list non-empty & deduped.
# 2. 50 random prompts per category contain no placeholders.
# 3. CLI `--dry-run` returns 0.
# 4. Plugin loader picks up new YAML on runtime.
# 5. Prompts1 corpus lines are reachable (sample subset).
#
# Merge & Review Protocol
# ───────────────────────
# 1. Disclose *function count* + *line count* for every revised script in PR body.
# 2. Attach coverage delta (`pytest-cov` output).
# 3. Reviewer runs:
#      pre-commit run --all-files
#      ./codex-merge-clean.sh $(git diff --name-only main..HEAD)
# 4. If merge artifacts remain, reject PR.
#
# Changelogs
# ──────────
# * Add entry to `0-tests/CHANGELOG.md` for multi-file changes.
# * Summarise outcome in `0-tests/task_outcome.md` post-merge.
#
# Authorization Guardrails
# ────────────────────────
# • Only operate on files/directories explicitly named in a work order.
# • Never bypass lint, dry-run, or coverage thresholds without written exception.
#
# End of AGENTS.md






















