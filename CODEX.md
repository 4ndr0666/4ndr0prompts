# CODEX.md

*Canonical Work Order & Audit Plan: Red-Team Prompt Mutation CLI Toolkit*

---

## 0. Mission & Executive Summary

This project delivers a fully agentic, **monolithic, audit-grade CLI** for red-team adversarial prompt generation. All UI/UX logic is centralized in a single Python entrypoint, using **prompt_toolkit** for an interactive, fuzzily-completed CLI that dynamically loads all categories and slots at runtime from a canonical dataset.

**Key business objectives:**
- Fully dynamic: categories/slots reflect dataset at runtime.
- UI/UX is driven *exclusively* by prompt_toolkit, with a unified color/style (#15FFFF).
- No fallback modes, no auxiliary files, no external UX/color imports.
- Entry is exclusively via `prompts.sh`, which auto-installs all Python dependencies.
- All prompts, audit logs, and output are traceable and adversarially robust.
- Complete test, lint, and automation coverage.
- Cross-functional review and audit rubric for acceptance.

---

## 1. Team Roles & RACI Matrix

| Task/Role               | Dev | QA | UX | Ops | Lead |
|-------------------------|-----|----|----|-----|------|
| CLI logic refactor      |  X  |    | X  |     |      |
| prompt_toolkit UX       |     |    | X  |     |      |
| Color scheme (#15FFFF)  |  X  | X  | X  |     |      |
| Dataset pipeline        |  X  | X  |    |     |      |
| Audit/automation infra  |     |    |    |  X  |      |
| Code review & doc       |  X  | X  | X  | X   |  X   |
| Roadmap/future          |     |    |    |     |  X   |

---

## 2. Deliverables & Acceptance Criteria

| ID  | Deliverable/Path              | Owner  | Key Acceptance Criteria |
|-----|-------------------------------|--------|------------------------|
| D1  | `promptlib_cli.py` (monolith) | Dev    | All CLI/UX logic centralized, prompt_toolkit only, #15FFFF scheme. No external logic/color imports. |
| D2  | `prompts.sh` (entrypoint)     | Dev    | Shell wrapper, auto-installs prompt_toolkit, launches CLI. |
| D3  | `dataset/templates.json`      | Dev    | All categories/slots loaded dynamically at runtime. |
| D4  | Unified cat/slot utilities    | Dev    | All menu/selection logic funneled through shared, auditable functions. |
| D5  | Style: #15FFFF everywhere     | UX     | All prompt_toolkit dialogs, completers, and messages use #15FFFF. |
| D6  | Fuzzy dynamic menus           | Dev/UX | All category/slot selection via FuzzyCompleter or WordCompleter. No static lists. |
| D7  | Prompt regeneration, preview  | Dev    | CLI lets user preview, regenerate, and accept/reject prompts. |
| D8  | Sample slot preview           | UX     | Example slot values always shown for each category. |
| D9  | Error handling                | QA     | All errors colorized, actionable, and visible. No silent failures. |
| D10 | Tests: 100% CLI/dataset paths | QA     | Automated tests exercise every CLI/dataset path. |
| D11 | README usage/docs             | Dev    | Up-to-date, explains CLI, data, auto-install, style, test, audit. |
| D12 | Automation scripts/hooks      | Ops    | Pre-commit, lint, test all enforced and pass. |

---

## 3. Task Breakdown & Technical Instructions

### **A. CLI Refactor & Color Unification**

**A.1. Style Block (Critical Completion)**
- All prompt_toolkit style entries (dialog, menu, completion, button, errors, arrows, highlights) must use #15FFFF as fg where possible.
- Example:

    ```python
    style = Style.from_dict({
        "dialog": "bg:#23272e #15FFFF",
        "dialog.body": "bg:#23272e #15FFFF",
        "dialog shadow": "bg:#23272e",
        "button": "bg:#15FFFF #23272e bold",
        "button-arrow": "#15FFFF",
        "dialog frame.label": "bg:#15FFFF #000000",
        "completion-menu.completion": "fg:#15FFFF bg:#23272e",
        "completion-menu.completion.current": "fg:#23272e bg:#15FFFF",
        # Extend for all prompt_toolkit elements in use
    })
    ```

- Review all `Style.from_dict` usage to guarantee compliance. No blue, green, or prior cyan.

**A.2. Fuzzy Menu Everywhere**
- All selection of categories/slots must use FuzzyCompleter (with WordCompleter).
- Example:

    ```python
    from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
    categories = get_categories_from_dataset()
    category = prompt(
        "Category:",
        completer=FuzzyCompleter(WordCompleter(categories)),
        style=style,
    )
    ```

**A.3. Unified Utility for Cat/Slot**
- Refactor to single utility module (internal only; no extra files), e.g.:

    ```python
    def get_categories(config):
        return sorted(config["templates"].keys())

    def get_slots(config, category):
        return sorted(config["slots"].get(category, {}).keys())
    ```

- **All menus must use these.**

**A.4. Slot Preview & Regeneration**
- When a category is chosen, immediately display a sample of slot keys/values.
- After previewing generated prompts, always offer to regenerate (new random slots) or accept/save.
- Loop until user accepts or cancels.

**A.5. Error Handling**
- All error dialogs use #15FFFF as highlight or error fg (bold, on dark bg).
- All error messages must show explicit actionable feedback (not just “failed”).
- Example: `"Category not found. Dataset may be outdated. Please update dataset/templates.json."`

### **B. Dataset & Pipeline Logic**

**B.1. Dynamic Dataset Loading**
- Categories/slots loaded on *every* CLI start (no static lists in code).
- Dataset changes reflect instantly on next CLI launch.
- No hardcoded category/slot names.

**B.2. Slot Randomization**
- For each prompt generation, slot values are selected randomly from available list, never repeated unless user requests.

### **C. Automation, Testing, and Documentation**

**C.1. Entry Script (prompts.sh)**
- Ensure prompts.sh:
  - Verifies prompt_toolkit, auto-installs if missing.
  - Invokes CLI Python monolith, passing all args.
  - Exits nonzero on error, logs all runs.

**C.2. Linting, Formatting, Automation**
- All code must pass: `black`, `ruff`, `shellcheck`, and all pre-commit hooks.
- All code, including shell, must have proper shebangs and be POSIX-compliant.

**C.3. Test Coverage**
- Tests must:
  - Invoke CLI for every menu/dataset path (batch and interactive).
  - Confirm all errors are colorized.
  - Cover audit log output, prompt regeneration, and slot randomization.

**C.4. Documentation**
- README must:
  - Show CLI/UX screenshots or asciinema (if possible).
  - Explicitly state use of #15FFFF style, prompt_toolkit, and monolithic policy.
  - List all categories/slots as loaded from current dataset.

---

## 4. Audit & Acceptance Rubric

- **Style**: Every CLI element, completion menu, dialog, and error must use #15FFFF.
- **UX**: All selection flows use prompt_toolkit prompt+completer, never static lists or input().
- **Dynamic Data**: No category or slot is hardcoded.
- **Monolith**: No new files for UX/color/style. All logic is in the main CLI file.
- **No Fallbacks**: No TUI/GUI; only CLI with prompt_toolkit.
- **Tests**: 100% coverage for all menu paths, errors, and output.
- **Automation**: Pre-commit, lint, and test must always pass.
- **Entry**: Only via prompts.sh.
- **Audit**: All output and errors logged; every prompt generation traceable.

---

## 5. Roadmap & Future Recommendations

### **A. Near-Term Enhancements**
- Add an optional CLI arg for instant dataset reload (for CI/CD, QA).
- Enable batch regeneration with configurable randomness (seed support).

### **B. Expansion/Long-Term**
- Wrap CLI in a lightweight HTTP API for automated or remote adversarial testing.
- Add plugin support for custom prompt mutations (via registered Python modules, loaded dynamically).
- Add user session analytics and reporting.
- Consider full internationalization (i18n) and accessibility color checks.
- Allow external style config (future, but must be justified for resource/perf).

### **C. Best Practices for Contributors**
- No new files for sharing code unless it measurably improves resource use or maintenance.
- All user-facing CLI text must pass color/style review before merge.
- Proposals for web/TUI/GUI require written justification of value and audit trace.

---

## 6. Ticketing Summary

1. **[D1]** Finalize promptlib_cli.py as monolith, using prompt_toolkit only and #15FFFF throughout.
2. **[D2]** Update prompts.sh to enforce dependency install, proper logging.
3. **[D3]** Refactor all cat/slot utilities into single (internal) block.
4. **[D4]** Confirm all menus use FuzzyCompleter, no static lists.
5. **[D5]** Add slot preview and regenerate loop for prompt generation.
6. **[D6]** Audit all error handling for color and actionable text.
7. **[D7]** Test: verify all paths, errors, slot randomization, audit log output.
8. **[D8]** README: Add explicit color/UX screenshots and current dataset snapshot.
9. **[D9]** Confirm pre-commit, ruff, black, shellcheck pass at all times.
10. **[D10]** Begin planning for API/plugin/i18n roadmap items.

---
