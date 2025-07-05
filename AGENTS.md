# 🚦 **Finalization Manifest: “4ndr0prompts” Red-Team Prompt System**

---

## Table of Contents

1. **Purpose & Context**
2. **Acceptance Criteria**
3. **Architecture Overview**
4. **Actionable Work Tickets**

   * \[A] Core Refactor & Feature Completion
   * \[B] CLI/UX/UI Finalization
   * \[C] Dataset, Plugin, and Hot-Reloading Infrastructure
   * \[D] Policy & Security Enforcement
   * \[E] Testing & QA Coverage
   * \[F] DevOps/Automation/Pre-commit
   * \[G] Documentation & User Guidance
   * \[H] Audit/Production Checklist
5. **Release Readiness Rubric**
6. **Roadmap & Further Enhancements**
7. **References & Supporting Materials**

---

## 1. 🎯 **Purpose & Context**

* This project aims to deliver a **unified, dynamic prompt generation CLI** for red-team, adversarial, and fuzzing use-cases, modeled on best-in-class interactive prompt engineering flows (e.g., Sora/Hailuo).
* All logic must be driven by canonical parameter libraries (`promptlib.py`), with runtime extension and hot-reload from plugin packs and datasets.
* The system must be **idempotent, strictly policy-compliant, and resistant to user error**—with an advanced CLI UX via `prompt_toolkit`.

---

## 2. ✅ **Acceptance Criteria** (Audit Rubric)

A release is “production ready” when ALL the following are true:

* [ ] **Promptlib, plugin, and dataset categories are fully canonical, deduped, and auto-loaded at runtime with hot-reload.**
* [ ] **Interactive CLI is fully keyboard-driven, with fuzzy-complete and colorized category/slot selection.**
* [ ] **No static UI logic; all menus/choices/validation derived from current data model and plugins.**
* [ ] **All error handling is colorized, actionable, and blocks further execution until fixed.**
* [ ] **No code changes required to add/remove/modify categories or slot options.**
* [ ] **All core commands, data loading, validation, and prompt assembly have test coverage.**
* [ ] **Pre-commit hooks enforce ruff, black, shellcheck, and pytest for every commit.**
* [ ] **All security/policy rules are strictly enforced, and adversarial prompts are shown verbatim.**
* [ ] **Documentation is current, clear, and covers setup, usage, dev workflow, and maintenance.**
* [ ] **Audit log/checklist is maintained and passed.**

---

## 3. 🏗️ **Architecture Overview**

* **`prompts.sh`**: Single user entrypoint, launches Python CLI with all required logic.
* **`promptlib.py`**: Canonical parameter library; all valid categories and slot options are defined here or dynamically loaded.
* **`plugin_loader.py`**: Loads and merges prompt options from JSON/YAML/Markdown plugin packs into normalized category mappings.
* **`canonical_loader.py`**: Exposes a hot-reloadable interface to parameter options, merging base and plugin data.
* **`promptlib_cli.py`**: Implements the interactive CLI (menus, previews, slot editing, save/copy).
* **`dataset/templates.json`**: Canonical dataset, merged and hot-reloaded with plugins.
* **Plugins directory**: All external prompt packs for red-team/adversarial extension.
* **Test suite**: Covers all category loading, menu flows, and prompt validation logic.
* **Pre-commit**: Automated enforcement of style, tests, and merge-artifact cleanup.

---

## 4. 🔖 **Actionable Work Tickets**

### \[A] CORE REFACTOR & FEATURE COMPLETION

#### A1. **Canonical Parameter Consistency & Hot-Reload**

* Ensure `promptlib.py`, `canonical_loader.py`, and `plugin_loader.py` support dynamic, zero-code-change slot/category extension.

  * [ ] Slot options, categories, and prompt templates must **never be duplicated or hardcoded** in multiple places.
  * [ ] All new plugin packs must be hot-reloadable into runtime menus.

#### A2. **Prompt Assembly Logic**

* Ensure **all prompt blocks are dynamically built** according to current options.
* Prompt assembly utilities must reject/flag any invalid or policy-violating values.

#### A3. **Dataset/Plugin Schema & Validation**

* Finalize strict schemas for base dataset and plugin formats (JSON/YAML/MD).
* Implement comprehensive input validation with actionable errors.

---

### \[B] CLI/UX/UI FINALIZATION

#### B1. **prompt\_toolkit-Driven Interactive Menu**

* CLI must:

  * [ ] Use **fuzzy-completer menus** for all categories and slots, using current runtime data.
  * [ ] Colorize completions, errors, and info per design (#15FFFF primary).
  * [ ] Always operate in TTY; print actionable error if not.
  * [ ] Regenerate previews on slot edit; allow users to save/copy/retry.
  * [ ] Respect all accessibility and keyboard usability best-practices.
* Implement clipboard copy for final output (with OS fallback if unavailable).

#### B2. **Error Handling & Policy Feedback**

* All error and warning messages must:

  * [ ] Be shown in color.
  * [ ] Halt progress until resolved.
  * [ ] Point to documentation if persistent.

---

### \[C] DATASET, PLUGIN, AND HOT-RELOADING INFRASTRUCTURE

#### C1. **Live Hot-Reload**

* Implement file-watch/hot-reload logic in `canonical_loader.py` for both `dataset/templates.json` and `plugins/`.
* Changes must reflect in CLI without process restart.

#### C2. **Plugin Loader Robustness**

* `plugin_loader.py` must:

  * [ ] Support JSON, YAML, and Markdown with code blocks (see \[461]).
  * [ ] Place unknown/extra fields into `uncategorized`, but never discard.
  * [ ] Deduplicate all entries while preserving order.

#### C3. **Plugin Format Documentation**

* Provide a reference template for plugin authors, with field descriptions, sample data, and troubleshooting guidance.

---

### \[D] POLICY & SECURITY ENFORCEMENT

#### D1. **Strict Policy Guardrails**

* Policy-violating (e.g. forbidden terms) prompts must:

  * [ ] Never be emitted without a red warning.
  * [ ] Always pass through strict regex and allowlist filters.
  * [ ] Never be autocorrected or sanitized silently.

#### D2. **Adversarial Prompt Transparency**

* All data—including misspellings, obfuscations, and adversarial content—must be **shown verbatim** with clear color-coded tags.

#### D3. **Audit Logging (Optional)**

* For advanced compliance, maintain an audit trail/log of user-generated prompts and actions (can be toggled in config).

---

### \[E] TESTING & QA COVERAGE

#### E1. **Automated Testing**

* Implement **pytest-based tests** covering:

  * [ ] All promptlib and plugin/category loading
  * [ ] All menu flows, slot editing, and prompt assembly
  * [ ] Policy enforcement and error handling
* **Coverage must be >90%**; critical logic paths must be exercised.

#### E2. **Manual QA Scripts**

* Provide CLI walkthrough scripts for QA.
* Test all “edge” cases, e.g.:

  * [ ] Adding a new plugin pack
  * [ ] Corrupt/malformed dataset or plugin file
  * [ ] Policy-violating/adversarial slot value

---

### \[F] DEVOPS/AUTOMATION/PRE-COMMIT

#### F1. **Pre-commit Hooks**

* Ensure `.pre-commit-config.yaml` covers:

  * [ ] `ruff` and `black` for Python
  * [ ] `shellcheck` for Bash
  * [ ] `pytest` for code
  * [ ] `0-tests/codex-merge-clean.sh` for artifact checks
* CI/CD must block merges on failures.

#### F2. **Artifact Scrubber**

* Any merged code or data must be automatically stripped of merge/backup artifacts.

---

### \[G] DOCUMENTATION & USER GUIDANCE

#### G1. **README & Usage**

* Update README to:

  * [ ] Reflect all new features, plugin flows, hot-reload, and error handling.
  * [ ] Provide “quickstart”, “advanced usage”, and “FAQ” sections.

#### G2. **Dev Docs**

* Maintain a **DEVELOPER.md** for:

  * [ ] Data model
  * [ ] Plugin formats
  * [ ] CLI/UI style guidelines
  * [ ] Testing, linting, and contribution workflow

#### G3. **User Help**

* CLI must offer inline help and direct links to documentation.

---

### \[H] AUDIT/PRODUCTION CHECKLIST

#### H1. **Final Release Readiness Audit**

* Maintain and complete an audit log for:

  * [ ] Parameter/category consistency across code, data, and docs
  * [ ] Zero hardcoded slot values in UI/logic
  * [ ] 100% policy filter coverage
  * [ ] Hot-reload verified for all data sources
  * [ ] CLI passes usability review (keyboard, error flows)
  * [ ] All tests/CI/pre-commit pass
  * [ ] Documentation up-to-date and matches product

---

## 5. 📝 **Release Readiness Rubric**

A release is approved only when:

| Rubric Item                   | Criteria                                             | Evidence             | Status |
| ----------------------------- | ---------------------------------------------------- | -------------------- | ------ |
| Canonical Parameter Model     | No dupe/missing categories or slot options           | audit, test logs     |        |
| Hot-Reload Data Infra         | No CLI restart needed for plugin/dataset change      | demo, test           |        |
| prompt\_toolkit UI            | Menus, errors, completions, colors all per spec      | video, UX script     |        |
| Policy & Adversarial Handling | Errors, warnings, and verbatim display per policy    | test, audit logs     |        |
| No Static UI Logic            | All menus auto-generated, no code changes for schema | code, test, review   |        |
| Automated & Manual Testing    | 90%+ coverage, edge-cases covered                    | pytest, manual logs  |        |
| Documentation                 | Complete, step-by-step, matches release build        | README, DEVELOPER.md |        |
| DevOps/Pre-commit             | All hooks pass, CI green                             | badge, logs          |        |
| Release Checklist Complete    | All items initialed by lead dev, QA, doc, PM         | audit log            |        |

---

## 6. 🚀 **Roadmap & Further Enhancements**

1. **REST API / Web UI**: Expose prompt generation and mutation as a RESTful service with web-based UX.
2. **Advanced Policy Engines**: Integrate external moderation services for real-time policy compliance and abuse/fuzz detection.
3. **Prompt Chain Graphs**: Visualize and track prompt mutations, dependencies, and test coverage over time.
4. **User/Team Profiles**: Per-user prompt history, favorites, and collaboration features.
5. **Export Formats**: Add export to JSONL, CSV, or direct to external tools for fuzz automation.
6. **Performance Profiling**: Benchmark menu/CLI loading with very large datasets/plugins.
7. **Accessibility Improvements**: Further keyboard shortcuts, font customization, and alternate color themes.

---

## 7. 📚 **References & Supporting Materials**

* See original code and supporting PDFs (camera\_movements.pdf, photography.md, sora\_prompting.md, etc).
* Consult README and developer docs for up-to-date usage and dev patterns.
* Refer to `promptlib.py`, `plugin_loader.py`, and `canonical_loader.py` for canonical logic.
* Example tickets and edge-case QA flows provided in `/0-tests/` and scripts.

---

### **Ticket Format (for Jira/GitHub/Notion etc)**

Each action item above is a ticket, cross-referenced with rubric line(s) and deliverable(s).
**Status** must be updated as work proceeds, with blockers/escalations noted.

---

# 🏁 **Final Notes: Execution Guidance**

* **Cross-functional execution** is required: assign infra, dev, QA, doc, and PM roles for each segment.
* Any change to the core schema or data model **must** be reviewed by at least two team leads.
* Keep all communication, commits, and doc changes transparent and attributed.
* The **audit log** and this manifest must be updated throughout execution and signed off before release.

---

This document, **when followed verbatim, will ensure the project’s completion to the original vision and highest professional standards**.
**All devs, QA, and docs must treat this as a living artifact** for the release process.

---

**End of Manifest**
