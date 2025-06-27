###############################################################################
# CODEX.md — Full Production Work Order: Red-Team Prompt Mutation Framework
# Project Codename: 4ndr0prompts
# Version: v1.0.0
# Last Updated: 2025-06-27
#
# This document defines a complete, cross-functional, team-executable
# implementation roadmap for converting the 4ndr0prompts repository into a
# fully-automated, reproducible, single-point UX system for adversarial
# prompt generation and NSFW stress testing.
#
# Conforms to:
# • XDG Base Dir Spec
# • ShellCheck POSIX standards
# • Python 3.10+, PEP 8 (ruff + black 88 cols)
###############################################################################

## 📌 OVERVIEW: Final System Goals

| Objective ID | Goal Description                                                                      |
|--------------|----------------------------------------------------------------------------------------|
| G1           | Create a SINGLE-ENTRY POINT interface (`prompts.sh`) that controls parsing, loading, UX |
| G2           | Eliminate ALL manual actions in category parsing and `templates.json` generation       |
| G3           | Remove legacy interfaces (npyscreen, deprecated CLI switches)                          |
| G4           | Align all slots/categories with `rawdata.txt` as the ONLY canonical source             |
| G5           | Dynamically adapt promptlib2 via live CATEGORY_MAP loading from templates.json         |
| G6           | Validate and fail safely when missing or malformed data is detected                    |
| G7           | Enable easy test, logging, and reproducibility workflows for devs                      |

---

## 🧠 SYSTEM COMPONENTS & LAYERS

| Layer            | Role                                                       | File(s)                                  |
|------------------|------------------------------------------------------------|------------------------------------------|
| 🧪 Data           | Canonical raw prompts, templates, and slot mapping         | `rawdata.txt`, `templates.json`          |
| 🧬 Parser         | Parses and generates slot/template JSON from raw text      | `scripts/parse_rawdata.py`               |
| 🧩 Loader         | Loads template data, randomizes, validates integrity       | `prompt_config.py`                       |
| 🧠 Generator      | Retrieves prompts by category from canonical sources       | `promptlib2.py`                          |
| 🧰 CLI UX         | Interactive interface with `prompt_toolkit` only           | `promptlib_cli.py`                       |
| 🚀 Entry Script   | Unified interface for automation, validation, UX           | `prompts.sh`                             |
| ✅ Testing        | Unit and functional tests for all layers                   | `tests/*.py`, `test_promptlib2.py`, etc. |
| 📊 Audit Tools    | Slot tracker, parse validation, logs, coverage reports     | `slots_report.tsv`, coverage tools       |

---

## 🛠️ ENGINEERING TASKS — PRIMARY IMPLEMENTATION

Each task is written for execution by a dedicated engineer or functional subteam.

---

### 🔧 TASK A — CLI Unification (UX Layer Owner)

**Owner:** UI Team  
**Status:** ✅ Done (needs validation)  
**Files:**
- `promptlib_cli.py`
- `prompts.sh`

**Steps:**
1. Remove all references to `--interactive`, `--cli`, `--tui`.
2. Delete deprecated files: `promptlib_tui.py`, `promptlib_interactive.py`, `promptlib_config.py`.
3. The only accepted interface is `prompt_toolkit`-based CLI.
4. Ensure `prompts.sh` launches it directly:
   ```bash
   python -m promptlib_cli
````

**Exit Criteria:**

* Launching `./prompts.sh` launches the CLI with prompt\_toolkit.
* No legacy interface artifacts are present.

---

### 🔁 TASK B — Slot and Template Auto-Refresh

**Owner:** Infrastructure / Backend
**Files:**

* `scripts/parse_rawdata.py`
* `dataset/rawdata.txt`
* `dataset/templates.json`
* `dataset/slots_report.tsv`

**Steps:**

1. Add a pre-launch hook to `prompts.sh` to auto-run:

   ```bash
   python scripts/parse_rawdata.py --write
   ```
2. Validate that it creates:

   * Updated `templates.json` (canonical slot/template structure)
   * Refreshed `slots_report.tsv` (audit)
3. Insert audit logging:

   * `log: dataset parsed @ timestamp`
   * If `templates.json` missing or malformed, fail safely.

**Exit Criteria:**

* Running `prompts.sh` always produces fresh slot/template data.
* Manual runs of `parse_rawdata.py` are unnecessary for users.

---

### 🔬 TASK C — Live Dynamic CATEGORY\_MAP

**Owner:** promptlib2 Dev Team
**Files:**

* `promptlib2.py`
* `prompt_config.py`

**Steps:**

1. Refactor `CATEGORY_MAP` in `promptlib2.py` to load from `prompt_config.load_config()["templates"].keys()`
2. Ensure this is always current with `templates.json` and has no hardcoded list.
3. Fallback: if loading fails, raise a fatal exception with helpful message:

   ```python
   raise RuntimeError("No valid category map found in templates.json")
   ```

**Exit Criteria:**

* `promptlib2.py` dynamically adapts to new categories automatically.
* Category list is always aligned with the dataset, no human touch required.

---

### 🚨 TASK D — Data Guardrails and Sanitization

**Owner:** Parser Team
**Files:**

* `scripts/parse_rawdata.py`

**Steps:**

1. Audit all default `category = "other_uncategorized"` assignments.
2. Add regex match-strength heuristic:

   * If >= 2 slot matches, assign best match.
   * Else: quarantine in `dataset/unassigned.tsv`
3. Warn when > 5% of prompts fall into `other_uncategorized`.

**Exit Criteria:**

* All prompts from rawdata are either classified or exported to unassigned.tsv.
* No prompt silently lands in undefined category.

---

### 🔍 TASK E — One-Shot Validation & Self-Healing

**Owner:** CLI & QA Team
**Files:**

* `prompt_config.py`
* `promptlib_cli.py`
* `prompts.sh`

**Steps:**

1. Add logic to fail gracefully if:

   * A slot referenced in template is not defined in `slots`
   * A category is empty or malformed
2. If mismatch found:

   * Log error to `var/error_log.txt`
   * Offer to regenerate from rawdata automatically
3. Insert `test_promptlib2.py` unit tests for slot presence:

   ```python
   assert slot in config["slots"][cat]
   ```

**Exit Criteria:**

* CLI never fails silently.
* Slot integrity is always ensured on runtime.

---

### 🧪 TASK F — Codebase Simplification & Cleanup

**Owner:** Tech Lead / Generalist
**Files:**

* `promptlib.py` (if deprecated)
* `promptlib2.py`
* `tests/`

**Steps:**

1. Confirm whether `promptlib.py` is still needed. If it’s fully duplicated by `promptlib2.py`, deprecate.
2. Consolidate duplicate imports across files.
3. Reorganize any test file under `tests/ui/` or `tests/core/` for clarity.

**Exit Criteria:**

* Only a single primary generator module remains.
* Folder structure is aligned to AGENTS.md.

---

## 🔒 TESTING REQUIREMENTS

| Test Type         | Tool       | Source File                   |
| ----------------- | ---------- | ----------------------------- |
| Unit Test         | `pytest`   | `tests/test_promptlib2.py`    |
| Slot Completeness | `pytest`   | `tests/test_rawdata_parse.py` |
| UX Launch         | shellcheck | `prompts.sh`                  |
| TTY Sanity        | `test -t`  | prompts.sh                    |
| Slot Regression   | `diff`     | slots\_report.tsv             |

---

## 📈 CI/CD & LINT

```bash
# lint
$ ruff --fix .
$ black .

# unit tests
$ PYTHONPATH=. pytest -q

# pre-commit
$ pre-commit run --all-files
```

> All commits must pass this minimum hygiene, or the PR is rejected.

---

## ✅ ACCEPTANCE RUBRIC (REQUIRED TO MERGE)

| Requirement                             | Description                                                    |
| --------------------------------------- | -------------------------------------------------------------- |
| 🔄 All prompts derived from rawdata.txt | templates.json and slots are machine-generated                 |
| ✅ One CLI-only UX entry                 | Only prompt\_toolkit CLI is usable                             |
| 🔁 No hardcoded CATEGORY\_MAP           | All categories are live-loaded                                 |
| 🧼 No deprecated codepaths              | TUI, CLI switches removed                                      |
| 🧪 Tests all pass on dry run            | `pytest -q` green                                              |
| 📦 Dataset reproducibility              | `parse_rawdata.py --write` produces identical output each time |
| 📄 AGENTS.md aligned                    | Directory + UX + dev patterns match AGENTS.md summary          |
| 📊 Logging enabled                      | Errors, generation, and slot drift logs are saved to `var/`    |

---

## 🧭 FUTURE ROADMAP

### 🔐 1. Prompt Signature Validation

* SHA256 hash every generated prompt
* Verify against known banned mutations
* Store logs under `var/audit_logs/YYYY-MM-DD-*.json`

### 🧩 2. Prompt Plugin Interface

* Allow Markdown plugins to inject categories/slots

### 📊 3. Dataset Dashboard

* Use `streamlit` to display category use frequency, slot collisions, coverage gaps

### 🧠 4. AI-Aided Categorizer

* Use fine-tuned GPT to auto-label uncategorized prompts

### 📦 5. Docker Package

* Package everything into CLI-only container
* Mount rawdata + output directory
