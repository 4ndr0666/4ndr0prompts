# 🚦 **CODEX.md — Final Audit Work Order (Red-Team Prompt Mutation Toolkit)**

```markdown
# CODEX.md

**Canonical Work Order and Sprint Execution Plan:**  
**Red-Team Prompt Mutation Toolkit (Monolithic, Dynamic, Audit-Grade)**

---

## 0. Mission Statement

Deliver a single-entry, prompt_toolkit-based CLI for adversarial prompt generation, built from a fully dynamic dataset with audit-traceable category/slot mapping, robust error handling, and zero fallback logic.  
All UX/UI, data, and logic are centralized—no extraneous modules or fallback paths.

---

## 1. Team RACI Table

| Task/Area                | Dev | QA | Ops | Lead | Doc |
|--------------------------|-----|----|-----|------|-----|
| CLI refactor (monolithic)|  X  |    |     |      |     |
| prompt_toolkit UX        |  X  |    |     |      |     |
| Data pipeline            |  X  | X  |     |      |     |
| Automation & infra       |     |    |  X  |      |     |
| Code review/audit        |  X  | X  | X   |  X   |     |
| Docs/workflow            |  X  |    |     |      |  X  |
| Roadmap/future           |     |    |     |  X   |     |

---

## 2. Deliverables Matrix

| ID  | Deliverable                     | Owner | Acceptance Criteria                                               |
|-----|---------------------------------|-------|-------------------------------------------------------------------|
| D1  | `promptlib_cli.py` (CLI)        | Dev   | All menu/UI/data/logic centralized; no external UX/color imports  |
| D2  | `prompts.sh` (entrypoint)       | Dev   | Auto-installs prompt_toolkit, launches CLI                        |
| D3  | `dataset/templates.json`        | Dev   | All categories/slots loaded dynamically, verbatim content         |
| D4  | Category/Slot utility           | Dev   | Unified internal utility; all menus use dynamic data              |
| D5  | Centralized color/style block   | Dev   | All dialogs share single style dict (top of CLI file)             |
| D6  | Fuzzy, live menus               | Dev   | All menus use prompt_toolkit fuzzy completer                      |
| D7  | Regenerate prompt feature       | Dev   | CLI supports prompt regeneration/review in-place                  |
| D8  | Slot preview in menus           | UX    | Slot/category previews in every menu                              |
| D9  | Robust error handling           | QA    | All errors colorized/actionable; invalid input = clear message    |
| D10 | Tests for CLI/dataset logic     | QA    | Full test coverage, all menu/data paths exercised                 |
| D11 | README, workflow documentation  | Dev   | Docs up-to-date, clear usage, all flows explained                 |
| D12 | Pre-commit automation           | Ops   | pre-commit, shellcheck, ruff, black enforced, codex-merge-clean   |

---

## 3. Task Breakdown & Technical Guidance

### **A. CLI Refactor & UI Centralization**

#### **A.1. CLI as Single UI/UX Source**

- All dialog, menu, selection, and error logic **must reside in promptlib_cli.py**.
- No external imports for color/style or dataset logic (except for data access from config).
- Fuzzy completion for all menu selection via prompt_toolkit.

#### **A.2. Unified Category/Slot Utility**

- One suite of functions in CLI for:
  - Fetching category list (from dataset/templates.json)
  - Fetching slot list per category
  - Previewing slots/examples in menu
- All menus must use these utilities to drive options.

#### **A.3. Centralized Color/Style Block**

- Place a single color/style dictionary at the top of CLI.
- All dialogs, errors, and prompts use this block—**team-editable**.

#### **A.4. Regenerate/Preview Features**

- User can preview and re-randomize prompts before saving.
- Slot previews always shown in selection dialogs.

---

### **B. Entrypoint and Automation**

#### **B.1. `prompts.sh` Entrypoint**

- Must:
  - Auto-install prompt_toolkit (robust Python inline check + pip install if needed).
  - Launch CLI script with all provided arguments.
  - Print actionable error and exit on any failure.

#### **B.2. Pre-commit/Lint/Automation**

- pre-commit config must enforce:
  - codex-merge-clean.sh (first)
  - ruff, black (Python)
  - shellcheck (Shell)
  - pytest (all paths)
- All code and shell scripts must be clean per linter.

---

### **C. Data Pipeline & Integrity**

- All dataset/templates are loaded at runtime from `dataset/templates.json`.
- Category and slot data are **verbatim** (misspelt, adversarial samples preserved).
- Slot/category mapping **never hard-coded**—always loaded dynamically.
- No TUI/GUI, fallback flows, or “simple-cli” in production CLI.

---

### **D. Test & QA Requirements**

- All test cases must:
  - Cover category/slot utility, prompt randomization, preview flows.
  - Assert that every slot/category in dataset is available in CLI menus.
  - Test error handling (missing category/slot/dataset).
  - Ensure no data is cleaned or sanitized at any pipeline stage.
- Audit logs written for every generation/output operation.

---

### **E. Documentation & Support**

- README.md must:
  - Clearly describe one-entry workflow, dynamic data, prompt_toolkit dependency.
  - Document how to regenerate dataset/templates.
  - List all available categories and show example slot mapping.
- CHANGELOG.md entry summarizing monolithic refactor and compliance.

---

### **F. Final Audit/Polish Checklist**

- [ ] Remove any legacy/unused files, TUI/GUI, or interactive fallbacks.
- [ ] Confirm all slot/category selection, fuzzy completion, and error logic is covered by tests.
- [ ] Run `pre-commit run --all-files` and `PYTHONPATH=. pytest -q` in clean environment.
- [ ] Add all changes to CHANGELOG.md with references to CODEX/AGENTS deliverables.

---

## 4. Future Roadmap & Contribution Rules

### **Roadmap/Enhancement Areas**

- API endpoint (Flask/FastAPI) for prompt serving, audit trail, and analytics.
- Live dataset hot-reload (auto-refresh CLI menus on file change).
- Prompt/session history, slot coverage analytics (within monolithic script).
- Internationalization (non-English datasets; extend slot/category dynamic mapping).

### **Contribution Rules**

- **No new UI or data files** unless justified for performance, security, or research.
- **All new logic must pass ruff, black, shellcheck, pytest, pre-commit.**
- **Security and research take priority over UX or convenience.**
- All code, commit, and PRs must reference this document and AGENTS.md for policy.

---

## 5. Audit Approval Rubric

- [x] All CLI, slot/category, and error logic is centralized and dynamic.
- [x] No fallback, TUI/GUI, or duplicate data flows.
- [x] All code and docs pass automation and style checks.
- [x] Every prompt, slot, and menu is audit-logged.
- [x] Adversarial and misspelt data is preserved end-to-end.

---

**Completion of this ticket signifies full compliance with both CODEX.md and AGENTS.md. All work and review should be traced against this doc for final audit.**
