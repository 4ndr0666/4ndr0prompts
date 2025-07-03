# AGENTS.md

---

# 🤖 **AGENTS.md — Best Practices and Enforcement Guidelines**

**Purpose:**
Defines strict best practices and enforcement guidelines for all code, agents, UIs, and contributors to the prompt engineering project. This file **must** be reviewed before any significant code, feature, or plugin change.

---

## 1. **Never Break The Canonical Chain**

* **All logic for option/parameter sourcing, prompt block assembly, and plugin ingestion must pass through:**

  * `promptlib.py` (all parameters, option sets, builders)
  * `plugin_loader.py` (all plugin packs, all categorization and dedupe)
  * `canonical_loader.py` (live reloading, parameter validation)
* **Never assemble prompts or option lists by hand.**
* **Never introduce new imports or files to "share" options—always go through canonical loader.**

---

## 2. **Prompt Toolkit and UX/UI Enforcement**

* **All CLI/TUI/UX flows must:**

  * Import their available options directly via `canonical_loader.py`.
  * Use **prompt\_toolkit** or equivalent for interactive flows, providing autocompletion and style.
  * No static option or category list in any CLI/TUI.
  * No fallback modes, legacy UIs, or alternate flows.
  * All error and validation messages must be colorized, actionable, and align with style guide (#15FFFF as primary highlight color).
  * All misspellings, adversarial, or malformed samples must be surfaced *verbatim* (for red team purposes).

---

## 3. **Automation, Lint, and Test Enforcement**

* **All code must be**:

  * Ruff/black/pyright/shellcheck clean.
  * Guarded by pre-commit hooks that enforce canonical chain, no hard-coded lists, no ad-hoc block assembly.
  * Tested for all dataset-driven paths.
  * Every new feature must provide new/updated tests (see `test_promptlib_cli_utils.py`).

---

## 4. **Plugin Ingestion and Validation**

* **All plugin files:**

  * Must be loaded only via `plugin_loader.py`.
  * Deduped and categorized at load time.
  * Rejected on parse or category error.
  * Cannot be used until reviewed and merged into canonical parameter set.

---

## 5. **Documentation, CI, and Approvals**

* **All documentation and code must:**

  * Explicitly declare their option sourcing and block assembly path.
  * Fail CI if any parameter or block comes from outside canonical chain.
  * Reference CODEX and AGENTS in code comments and PR summaries.

---

## 6. **Security and Adversarial Integrity**

* **Security always trumps convenience:**

  * Any proposal to break monolithic structure must show measurable resource/performance gain and undergo security review.
  * All adversarial/edge case samples must be supported, visible, and tested in the UX chain.

---

## 7. **Change Management and Future-Proofing**

* **Any new prompt type, parameter, or UX flow must:**

  * Be proposed as an extension to `promptlib.py`, with new builder/validator logic.
  * Provide plugin pack in supported format (MD/YAML/JSON) with category and dedupe rules.
  * Document test coverage and update audit scripts as needed.

---

## 8. **Approval Rubric and Ticketing**

* **Any PR, plugin, or UX change is only approved if:**

  * All logic, validation, and UX flows use canonical chain exclusively.
  * Full test coverage of new/changed parameter(s) or blocks.
  * Updated documentation and changelog.
  * Reference to CODEX/AGENTS and relevant ticket IDs in all commit and PR messages.
  * Final review and sign-off from project leadership.

---

## 9. **Further Enhancements and Roadmap**

### Immediate:

* Migrate any remaining legacy scripts to canonical chain.
* Integrate plugin hot reload triggers for all UIs.
* Expand plugin schema as needed for new genres or prompt types.

### Mid-Term:

* Add live audit dashboard and parameter diff tool.
* Build automated adversarial test case generator.

### Long-Term:

* Move toward fully self-healing plugin chain and automated UX adaptation to new parameters.

---

**This AGENTS.md is a living document. All contributors are expected to help maintain and enforce its standards.
Any deviation is grounds for review and, if necessary, reversion or escalation.**
