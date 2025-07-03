# CODEX.md — Red-Team Prompt Mutation Toolkit (Final Sprint Work Order)

---

## **0. Mission Statement & Sprint Objective**

> **Mission:**
> Deliver a monolithic, prompt\_toolkit-powered adversarial prompt aggregator for red team prompt mutation, with dynamic category/slot mapping from a canonical dataset, randomized slot selection, and audit-robust logging.
> No fallback or redundant UI/UX code paths. All logic, dataset handling, and interface workflows must be centralized, maintainable, and dynamically data-driven.

---

## **1. RACI Table — Roles and Responsibilities**

| Task Area              | Dev | QA | UX | Docs | Ops | Lead |
| ---------------------- | --- | -- | -- | ---- | --- | ---- |
| CLI/UI refactor        | X   |    | X  |      |     |      |
| Dataset/dynamic loader | X   | X  |    |      |     |      |
| Slot/category utils    | X   |    |    |      |     |      |
| Audit logging          | X   | X  |    |      |     |      |
| Test suite/coverage    |     | X  |    |      |     |      |
| Automation/lint/CI     | X   |    |    |      | X   |      |
| Documentation          |     |    |    | X    |     |      |
| Review/merge           |     |    |    |      |     | X    |
| Roadmap/future         |     |    |    |      |     | X    |

---

## **2. Deliverable Matrix (D#) — Acceptance Criteria**

| ID  | Deliverable / Path           | Owner | Acceptance Tests / Criteria                                                |
| --- | ---------------------------- | ----- | -------------------------------------------------------------------------- |
| D1  | `promptlib_cli.py` (sole UI) | Dev   | Only CLI entrypoint, all menu/UI logic centralized, no imports for UI/UX   |
| D2  | `prompts.sh` (entrypoint)    | Dev   | Auto-installs prompt\_toolkit, only runs monolithic CLI, no fallback flags |
| D3  | Category/slot utilities      | Dev   | All dynamic, menu-agnostic, support fuzzy search, slot previews            |
| D4  | Dataset loader/validator     | Dev   | Always loads fresh from dataset/templates.json, audits new categories      |
| D5  | Fuzzy, dynamic menus         | Dev   | All menus use prompt\_toolkit fuzzy completer, preview sample slot values  |
| D6  | Robust audit logging         | Dev   | All generation is logged (category, slot, timestamp, prompt text)          |
| D7  | Unified color/style block    | Dev   | All dialogs/menus use centralized, reusable style dict, no color imports   |
| D8  | README/docs                  | Docs  | Only references canonical CLI, single workflow, dataset-driven operation   |
| D9  | Test suite/coverage          | QA    | Tests all menu, dataset, and error paths; audit log coverage               |
| D10 | Pre-commit/CI automation     | Ops   | Lint, black, ruff, shellcheck, and tests run for all PRs                   |

---

## **3. Technical Task Breakdown & Instructions**

---

### **A. Monolithic CLI/UI Refactor**

#### **A1. Delete/Consolidate All UI Files**

* **Delete**: `promptlib_interactive.py`, `promptlib_tui.py`, and any code referencing TUI/GUI or “--simple-cli”.
* **Migrate**: Any unique features or logic from these files *must* be ported to `promptlib_cli.py` before deletion.
* **Retain**: Only `promptlib_cli.py` as the interactive menu interface.
* **No fallback or alternate entrypoints** are allowed (per AGENTS.md).
* **Acceptance Test**: Only `promptlib_cli.py` runs as interactive menu; no code or docs reference TUI/interactive/fallback flows.

#### **A2. Centralize All Menu/Prompt Logic**

* **All** input dialogs, menus, slot selectors, previews, error messages, and colored status lines must be implemented in `promptlib_cli.py`.
* **Menu code must use prompt\_toolkit**: Utilize dialog, list, input, and confirmation widgets for each step (category, slot, count, preview, save).
* **All error paths and confirmations** must be colorized using a centralized style dictionary.

#### **A3. Single Source of Data: Dynamic Loader**

* All category/slot data must come dynamically from `dataset/templates.json` at runtime, via a loader utility (either as internal function or `prompt_config.py` import).
* No hard-coded lists. Menus, previews, slot suggestions all reflect latest dataset.
* Loader must validate and warn if new categories or slots are found (and log them).
* Loader must gracefully handle missing, corrupt, or misaligned dataset files.

---

### **B. UX/UX Polish and Dynamic Dataset Mapping**

#### **B1. Fuzzy Completer for Menus**

* **All category and slot menus** must use prompt\_toolkit’s `FuzzyCompleter` for rapid, typo-tolerant searching (test with >50 categories/slots).
* On selection, menu must show **sample slot values** in preview (at least 2-3 real examples, not placeholder text).

#### **B2. Unified Style and Error Handling**

* Define a **single, reusable style dictionary** at the top of `promptlib_cli.py`.

  * Example:

    ```python
    COLOR_STYLE = {
        "dialog": "bg:#222222 #ffffff",
        "button": "bg:#003366 #ffcc00 bold",
        "error": "bg:#ff0033 #ffffff bold"
    }
    ```
* All dialogs and prompts must use this dictionary; no in-line or repeated color codes.
* All error messages and “success” banners must be colorized.
* All invalid/missing/unknown category or slot selections must produce clear, actionable error dialogs and audit logs.

---

### **C. Audit-Grade Logging and Output**

#### **C1. Structured, Tamper-Resistant Audit Logs**

* All prompt generations (category, slots, full prompt text, timestamp) must be logged to a unique audit log file in a protected directory (e.g., `~/.local/share/redteam-prompts/logs/prompt_audit.log`).
* All log writes must be append-only and flush immediately.
* All prompt outputs must include category, slots, and full text.
* If file/dir creation fails, surface error to user with colorized message and audit the failure.

#### **C2. Output Structure**

* Generated prompts must be saved as:

  * Human-readable .txt files per category and session
  * Audit logs in TSV/JSONL or similar (timestamp, category, prompt, slots)
  * Optionally, display and confirm save location to user
* Directory creation must be automated; no manual setup.

---

### **D. Automation, Linting, CI/CD**

#### **D1. `prompts.sh` Entrypoint**

* Must check for Python 3.10+, prompt\_toolkit, and all required dependencies.
* If missing, **auto-install prompt\_toolkit** using pip before launching CLI.
* No reference to “--tui”, “--interactive”, or legacy flags.
* Always calls `promptlib_cli.py` as the single UI.
* **Acceptance**: Shellcheck clean, ruff/black clean, and pre-commit enforced.

#### **D2. Lint, Formatting, and Automation**

* All Python: PEP8, ruff/black clean.
* All shell: POSIX, shellcheck, shfmt clean.
* All scripts require `#!/usr/bin/env` shebang.
* All merge-conflict artifacts must be cleaned using `0-tests/codex-merge-clean.sh`.
* Pre-commit config must include ruff, black, pytest, shellcheck, and merge-clean hooks.
* All automation scripts must reside in `/0-tests` or `/scripts`.

---

### **E. Test Suite Expansion**

#### **E1. Dataset and Menu Path Coverage**

* All menu paths, slot selections, category choices, and error paths must be exercised in tests.
* Use mocks or test harnesses to automate selection and validation.
* **Acceptance**: `pytest -q` passes 100%; `PYTHONPATH=. pytest -q` is documented.

#### **E2. Fuzzy Search and Slot Preview Test**

* Add tests to verify:

  * Fuzzy search matches substrings, typos.
  * Slot previews display the expected values for the category chosen.
  * Invalid/unknown slot or category selection yields proper error and log entry.

#### **E3. Audit Log Integrity**

* Tests must ensure that:

  * All generations are logged (category, slot, prompt, timestamp).
  * Log entries are append-only and well-formatted.
  * Audit log file is created if missing, and error if permissions fail.

---

### **F. Documentation**

#### **F1. README.md**

* Remove any reference to legacy UI or TUI interfaces.
* Document:

  * Only one entrypoint: `prompts.sh`
  * All dataset and slot logic is dynamic and centralized
  * How to update dataset/templates.json and see menu auto-update
  * Example CLI flows, expected file outputs, and error paths
* Document all test, lint, and audit commands.

#### **F2. Inline CLI --help**

* The `--help` flag for both CLI and shell scripts must display all required options, argument details, and usage examples.
* Usage block should always print list of available categories (fetched from dataset, not hard-coded).

---

## **4. Further Enhancements / Roadmap**

### **G.1. Optional (for future sprints, not this release)**

* **REST API Layer:**
  Expose prompt generation over HTTP via Flask/FastAPI, returning audit logs as JSON.
* **Live Dataset Reload:**
  Watch for changes in `templates.json` and auto-refresh menu without restarting CLI.
* **Session Analytics:**
  Generate coverage reports, per-category stats, and slot usage graphs.
* **Internationalization (i18n):**
  Support for multi-language prompt/slot values and UI strings.
* **Pluggable Slot Extractors:**
  Allow research plugins to inject new categories/slots from custom datasets.

---

## **5. Audit & Production Approval Rubric**

1. **Monolithic Structure:**

   * Only `promptlib_cli.py` serves as UI; all other interactive files deleted.
2. **No Redundant I/O:**

   * No additional UI, color, or dataset-sharing files.
3. **Full Fuzzy Menus:**

   * Fuzzy completer in all selection steps; slot previews present.
4. **Dynamic Dataset:**

   * Changing `templates.json` instantly updates menus without code changes.
5. **Error Handling:**

   * All errors are colorized and actionable; all failed actions logged.
6. **Test Coverage:**

   * All menu and prompt flows are tested; coverage must be reported.
7. **Docs & CLI Usage:**

   * Only a single path for use; README/--help are accurate and up to date.
8. **Pre-commit Hooks:**

   * All lint, format, merge-artifact and test hooks run clean.
9. **Audit Logs:**

   * All generations and errors logged with timestamp, category, and prompt text.

**Any PR that fails any of the above must be rejected.**

---

## **6. Ticketing Summary (Ready for Delegation)**

1. **\[D1] Refactor and centralize all CLI/UI logic in promptlib\_cli.py.**

   * Remove TUI/interactive/legacy files; port useful code.
   * Confirm all input/output/error logic is present.

2. **\[D2] Confirm prompts.sh only launches promptlib\_cli.py, auto-installs prompt\_toolkit, and passes all arguments.**

3. **\[D3] Consolidate all category/slot utilities in promptlib\_cli.py, no redundant code.**

4. **\[D4] Implement fuzzy search and dynamic slot preview in all menus.**

5. **\[D5] Centralize style dict, colorize all output and errors, remove any hard-coded color logic.**

6. **\[D6] Expand and document test suite for menu path, slot preview, error, and log integrity.**

7. **\[D7] Update all documentation, README, and --help text to reflect new workflow.**

8. **\[D8] Ensure pre-commit, lint, and CI/CD pipelines enforce all of the above.**

9. **\[D9] Draft a roadmap (in CHANGELOG or CODEX) for optional API/web, i18n, or analytics features.**

---

## **7. Acceptance Procedure (QA/Lead)**

* On PR, lead must check:

  * [ ] No UI fallback or legacy flows exist
  * [ ] Dataset changes reflected live
  * [ ] Fuzzy search and slot preview work
  * [ ] Audit log and outputs are correct
  * [ ] All tests, lint, and automation pass
  * [ ] Docs and help match production flow
  * [ ] Only `promptlib_cli.py` is entrypoint for menu/UI

* **Reject** any PR not meeting above criteria.

---

**End of CODEX.md — Assign each \[D#] to named team member(s) and proceed.**
