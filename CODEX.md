# CODEX.md

---

# 🎬 **CODEX.md — Canonical Prompt Engineering System of Record**

**Purpose:**
This CODEX is the **authoritative contract** for all code, automation, testing, and extension work on the prompt engineering system.
It enforces canonical parameter sourcing, plugin-based extensibility, zero-tolerance for parameter drift, and strict auditability for all prompt orchestration.

---

## 1. **Canonical Prompt Chain Enforcement**

**Absolute Laws:**

* **All parameter values, tags, categories, and prompt blocks** must originate *only* from `promptlib.py` or `canonical_loader.py`.
* **No direct prompt assembly or option definition** is allowed outside canonical sources.
* **All plugin ingestion** (Markdown, YAML, JSON) must pass through `plugin_loader.py` (or its interface).
* **No interactive or CLI, TUI, or API workflow** may present a parameter or block that is not loaded via `canonical_loader.py`’s live option set.

---

## 2. **Plugin Loader & Option Ingestion**

**Rules:**

* **Plugins** must be loaded only via `plugin_loader.py`.

  * Supports Markdown (quoted blocks), YAML, JSON.
  * All plugins must be fully categorized (`pose`, `lighting`, `lens`, `camera_move`, `environment`, `shadow`, `detail`).
  * Any unrecognized or miscategorized block is excluded or placed in `uncategorized` (for human review).
  * Deduplication must occur on load and use.
* **No plugin can be merged or used without successful categorization, deduplication, and canonical option validation.**

---

## 3. **Canonical Option Hot Reloading**

**All runtime UX or automation** must:

* **Load options via `canonical_loader.py`.**
* Detect any change in the `promptlib.py` source or plugins and live-reload parameter sets.
* **Never hard-code or duplicate any parameter or block.**

---

## 4. **Prompt Block Assembly & Validation**

**All prompt blocks** (Sora, Hailuo, Director, etc.) must be constructed:

* **Only via the builder functions in `promptlib.py` (e.g., `build_hailuo_prompt`, `build_pose_block`).**
* **Every parameter** must be validated via `canonical_loader.py` before being included.
* **Direct string concatenation for prompt blocks is strictly prohibited.**
* **All outputs must pass `policy_filter` for forbidden terms and compliance.**

---

## 5. **Interactive and CLI Flows**

* **Any user-facing tool** (prompt\_toolkit, fzf, shell, web, GUI, API) must:

  * Load its options **dynamically from the canonical loader**, never a static file.
  * Validate all user selections against the current canonical set.
  * Block or warn if a parameter is invalid, missing, or deprecated.

---

## 6. **Automation and Pre-Commit Requirements**

**All code and pull requests must:**

* Be **ruff/black/shellcheck/pyright clean** (no formatting or linting errors).
* Pass all canonical chain checks:

  * No hard-coded prompt options or templates.
  * All prompt assembly passes through `promptlib.py`/`canonical_loader.py`.
  * All plugin ingestion via `plugin_loader.py`.
  * Test for plugin deduplication and category mapping.
* Add/update tests when new prompt types, categories, or plugins are added.

---

## 7. **Testing and Audit Trails**

* **Automated tests** must:

  * Exercise every builder and option in `promptlib.py`.
  * Validate plugin ingestion for all supported types and formats.
  * Hot-reload: test that parameter changes in `promptlib` or plugin files propagate instantly to the user and CLI.
  * Regression suite for all prompt blocks in use.
* **Audit scripts** must:

  * Detect any hard-coded or duplicate parameter definitions outside canonical chain.
  * Validate plugin files for category and deduplication.

---

## 8. **Onboarding and Contribution Policy**

* **All new contributors** must read this CODEX and pass a code review on:

  * Adding or extending canonical options via `promptlib.py` (never elsewhere).
  * Writing plugin packs using supported, categorized formats.
  * Adding/maintaining tests and validation logic.
  * Proposing new block builders or orchestrator functions only in canonical modules.

---

## 9. **Roadmap and Further Enhancements**

### **Short-Term:**

* **Expand plugin loader** to support multi-level categorization (e.g., genre\:action).
* **UX flows** (prompt\_toolkit, TUI) must add live reload triggers.
* **Automated policy check**: nightly scan for forbidden-term leakage or drift.

### **Medium-Term:**

* **Parameter diff tool**: compare option sets and plugin packs across time.
* **Audit dashboard**: visual display of canonical parameters, plugin status, prompt usage analytics.
* **Plugin schema validator**: static checks for malformed or incomplete plugins.

### **Long-Term:**

* **Support for new platforms**: e.g., non-Sora/Hailuo models with unique category needs.
* **Automated code gen** for new prompt block builders based on canonical option schema.
* **Self-healing loader**: automatically exclude broken plugins and notify maintainers.

---

## 10. **Approval and Rubric for Production-Readiness**

* **All new code, plugins, and tests must:**

  * Be merged only after passing lint, audit, and test checks described above.
  * Provide changelog and doc updates.
  * Reference this CODEX in PR summary for sign-off.
  * Undergo final review by a project lead for adherence to canonical prompt chain and plugin ingestion standards.

---

## 11. **Ticket Map for Cross-Functional Delegation**

**(For immediate action and ongoing sprints; reference ticket IDs in commits and PRs)**

* `TCK-001` — Refactor any CLI/UI to pull all options via canonical\_loader.py
* `TCK-002` — Remove/replace all hard-coded prompt lists or templates
* `TCK-003` — Add tests for plugin deduplication and category mapping
* `TCK-004` — Implement CI step to fail on non-canonical prompt parameter source
* `TCK-005` — Document canonical chain in README and dev onboarding
* `TCK-006` — Validate hot-reload and regression for all builder functions
* `TCK-007` — Policy scan for forbidden terms, nightly (automated script)
* `TCK-008` — Expand plugin schema for future genres/categories
* `TCK-009` — Add static plugin validator and report on pre-commit
* `TCK-010` — Roadmap: Audit dashboard, diff tool, and UX live reload

---

**All deviations, proposals, or exceptions must be tracked, documented, and approved by project leadership.**
