# CODEX.md

*Canonical Work Order and Execution Plan: Red-Team Prompt Mutation Toolkit*

---

## 0. Mission Statement

This sprint delivers a fully agentic, monolithic, high-performance prompt mutation toolkit with **verbatim, dataset-driven adversarial prompt generation**.
All UI/UX logic and styling are centralized, using **prompt\_toolkit** for CLI. The entrypoint is `prompts.sh` (which auto-installs dependencies as needed), and all menu/category/slot logic is dynamic, driven by canonical data.
**No extraneous files or I/O** are permitted for UI or style sharing.
All deliverables are actionable and cross-referenced for team members.

---

## 1. Team Roles & RACI

| Role/Task          | Dev | QA | UX | Ops | Lead |
| ------------------ | --- | -- | -- | --- | ---- |
| CLI refactor       | X   |    | X  |     |      |
| prompt\_toolkit UX |     |    | X  |     |      |
| Data pipeline      | X   | X  |    |     |      |
| Automation & infra |     |    |    | X   |      |
| Code review/audit  | X   | X  | X  | X   | X    |
| Docs               | X   |    |    |     | X    |
| Roadmap/future     |     |    |    |     | X    |

---

## 2. Deliverable Matrix

| ID  | Deliverable/Path                | Owner | Key Acceptance Tests/Criteria                          |
| --- | ------------------------------- | ----- | ------------------------------------------------------ |
| D1  | `promptlib_cli.py` (monolithic) | Dev   | All logic centralized, no imports for style/logic      |
| D2  | `prompts.sh` (entrypoint)       | Dev   | Auto-installs prompt\_toolkit if missing, launches CLI |
| D3  | `dataset/templates.json`        | Dev   | All categories/slots loaded dynamically                |
| D4  | Category/Slot utility           | Dev   | Unified function suite, all menu input calls it        |
| D5  | Centralized color/style block   | Dev   | All dialogs share one style dict, no external files    |
| D6  | Dynamic, fuzzy, live menus      | Dev   | Menus auto-update on dataset changes                   |
| D7  | "Regenerate prompt" feature     | Dev   | CLI can reshuffle, show prev/next                      |
| D8  | Sample slot preview in menus    | UX    | User sees examples before picking                      |
| D9  | Robust error handling           | QA    | Any missing category/slot triggers colored error       |
| D10 | Tests for CLI & dataset logic   | QA    | 100% menu path coverage, dataset changes tested        |
| D11 | README usage & workflow         | Dev   | Describes entry, auto-install, dynamic logic           |
| D12 | Automation/infra scripts        | Ops   | Pre-commit, lint, test, no fallback modes              |

---

## 3. Task Breakdown & Technical Explanation

### **A. CLI Refactor & Monolithic Design**

#### **A.1. Centralize All UI/UX Logic**

* Refactor `promptlib_cli.py` to encapsulate:

  * All menu, dialog, and prompt flows
  * All prompt\_toolkit logic (input, color, completion)
  * Category/slot dataset handling, fuzzy search, and preview
* **No imports** for UI/UX, style, or dataset logic from outside files
* Example:

  ```python
  # At top of promptlib_cli.py
  COLOR_STYLE = {
      "dialog": "bg:#212121 #ffffff",
      "button": "bg:#003366 #ffcc00 bold",
      "error": "bg:#ff0033 #ffffff bold"
      # ...
  }
  ```

#### **A.2. Shared Category/Slot Utility**

* All category/slot retrieval, validation, and selection logic in a single function suite.

* Every menu/selection calls this, e.g.:

  ```python
  def get_categories(config):
      return sorted(list(config["templates"].keys()))
  def get_slots(config, category):
      return sorted(list(config["slots"].get(category, {}).keys()))
  ```

* **All menus and prompts use these functions.**

#### **A.3. Fuzzy Search & Preview in Menus**

* Use prompt\_toolkit’s `prompt_toolkit.shortcuts.prompt` with fuzzy completer:

  ```python
  from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
  category = prompt("Category:", completer=FuzzyCompleter(WordCompleter(get_categories(config))))
  ```

* When a category is selected, show slot examples:

  ```python
  sample_slots = ', '.join(config["slots"].get(category, {}).keys()[:3])
  print(f"Sample slots: {sample_slots}")
  ```

#### **A.4. "Regenerate Prompt" Feature**

* After prompt generation, provide `[Enter] to regenerate, [q] to quit`:

  ```python
  while True:
      prompt = generate_prompt(...)
      print(colored(prompt, "green"))
      action = prompt("Press Enter to regenerate, q to quit: ")
      if action.lower() == "q":
          break
  ```

#### **A.5. Robust Error Handling**

* Every user input path checks for missing/invalid dataset, category, slot.
* If error, show prompt\_toolkit colored dialog with error style and clear next steps.

---

### **B. Entrypoint & Automation**

#### **B.1. `prompts.sh` Entrypoint**

* Only launches `promptlib_cli.py`, passes through args.
* On startup, checks for prompt\_toolkit:

  * If missing, **attempts auto-install** (`pip install prompt_toolkit`), warns and exits if fails.
* Example:

  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  if ! python3 -c "import prompt_toolkit" 2>/dev/null; then
      echo "prompt_toolkit missing. Attempting install..."
      python3 -m pip install prompt_toolkit || { echo "Install failed!"; exit 1; }
  fi
  exec python3 promptlib_cli.py "$@"
  ```

#### **B.2. No Fallback Modes**

* No TUI, no "interactive" shell, no alternate code paths.
* All UI/UX in one CLI, all logic in one script.

#### **B.3. Automation & Infra**

* All lint/test/QA in pre-commit.
* No I/O wasted on unnecessary files—single point of truth per script.

---

### **C. Dataset Intelligence & Dynamic UX**

#### **C.1. Dynamic Loading**

* Every CLI invocation loads the latest `dataset/templates.json` for categories/slots.
* Any update to the dataset is immediately reflected in UI.

#### **C.2. Slot Value Intelligence**

* When a user is choosing a slot, show examples pulled from the config file, e.g.:

  ```
  Slot: CLOTHING_TOP (Examples: "dress", "top garment")
  ```

#### **C.3. Fuzzy Search for Large Datasets**

* Use FuzzyCompleter to support fast lookup and selection even as dataset grows.

---

### **D. Documentation & QA**

#### **D.1. README.md**

* Clearly describe:

  * `prompts.sh` as the entrypoint
  * Auto-installation of dependencies
  * Monolithic, dynamic, audit-grade data pipeline
  * Usage examples, including how to regenerate dataset and run all tests

#### **D.2. Test Suite**

* QA must verify:

  * Every menu path, category/slot selection
  * CLI prompt logic after dataset change
  * Prompt regeneration/fuzzing
  * All error paths (missing dataset, invalid slot, etc.)

#### **D.3. Pre-commit/Lint**

* Ensure all code is `ruff` and `black` compliant
* All scripts with shebang and proper permissions

---

### **E. Roadmap & Future Enhancements**

#### **E.1. Roadmap**

* API wrapper (Flask/FastAPI) for exposing prompt generation via HTTP
* Live dataset update notifications (watch `templates.json`)
* Session logging for prompt history and user actions (for research)
* Optional advanced UX: progress bars, analytics, slot coverage metrics
* Internationalization and accessibility features

#### **E.2. Recommendations for Future Contributors**

* All new logic must be integrated into the monolithic CLI script unless storage/data pipeline demands otherwise.
* All dataset, category, and slot logic must remain fully dynamic and never hardcoded.
* Any proposal for TUI/GUI or web frontend must demonstrate value over CLI-only model before being approved.
* Prioritize UX and automation, but **never add files just for code sharing**.
* Security: never auto-correct data; always keep misspellings and adversarial samples verbatim.

---

## 4. Audit & Approval Rubric

* All logic for category, slot, dataset, and UI must exist in `promptlib_cli.py`.
* No auxiliary files for color/style/util logic.
* Entry and exit always via `prompts.sh` calling the CLI.
* No import errors or dependency issues—`prompt_toolkit` is always present or auto-installed.
* Any menu/list is 100% dataset-driven and fuzzy-searchable.
* All prompt generation and slot/category actions are audit-traceable.
* No hidden fallback code paths, only one canonical flow.
* Tests and pre-commit hooks must cover every action path.
* Documentation is clear and current.

---

## 5. Examples (for reference)

**A. Central Style Block**

```python
COLOR_STYLE = {
    "dialog": "bg:#222222 #ffffff",
    "button": "bg:#003366 #ffcc00 bold",
    "error": "bg:#ff0033 #ffffff bold"
}
```

**B. Fuzzy Menu**

```python
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
category = prompt("Category:", completer=FuzzyCompleter(WordCompleter(get_categories(config))))
```

**C. Slot Preview**

```python
slot_examples = ', '.join(config["slots"][category][slot][:2])
print(f"Slot: {slot} (Examples: {slot_examples})")
```

**D. Auto-Install Dependency**

```python
try:
    import prompt_toolkit
except ImportError:
    import subprocess, sys
    print("prompt_toolkit not found, installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "prompt_toolkit"])
    import prompt_toolkit
```

---

## 6. Ticketing Summary

1. **\[D1] Refactor and centralize all CLI/UI logic in promptlib\_cli.py.**
2. **\[D2] Optimize prompts.sh for auto-install and single-path entry.**
3. **\[D3] Implement all category/slot utilities internally in CLI.**
4. **\[D4] Add fuzzy search and slot preview in all menus.**
5. **\[D5] Ensure robust error handling and 100% dynamic dataset logic.**
6. **\[D6] Update all documentation and tests for the new flow.**
7. **\[D7] Plan for future API/UX expansion but keep all enhancements monolithic until justified.**
