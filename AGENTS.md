## 🗒️ **Sprint Tasks**

### 📌 **200-001 · SHE · Restore Minimal CLI (`bin/prompts.sh`)**

* **Goal:** Ensure slot-by-slot fzf-based interactive mode with wl-copy clipboard only.
* **Acceptance Criteria:**

  * Prompts each slot in order as aggregated /home/git/clone/4ndr0prompts/plugins/prompts1.md.
  * Copies final assembled prompt via `wl-copy`.
  * Exits gracefully with error if `wl-copy` is missing.

---

### 📌 **200-002 · PYL · Validate Slot Canonicalization (`promptlib.py`)**

* **Goal:** Ensure slots/categories are directly aggregated from /home/git/clone/4ndr0prompts/plugins/prompts1.md and defined once in Python, no external YAML/JSON.
* **Acceptance Criteria:**

  * Defines `SLOTS` clearly with slot-order enforced and directly aggregated from /home/git/clone/4ndr0prompts/plugins/prompts1.md.
  * Raises errors on duplicates or invalid values.
  * No external data files required at runtime.

---

### 📌 **200-003 · QA · Restore Bats Test Suite (`tests/cli.bats`)**

* **Goal:** Automate interactive flow testing.
* **Acceptance Criteria:**

  * Simulates user input for each slot via dummy `fzf`.
  * Verifies clipboard functionality via `wl-copy` simulation (`wl-paste`).
  * All tests pass via `make test`.

---

### 📌 **200-004 · DOC · Minimal README and Usage Docs**

* **Goal:** Provide succinct, accurate instructions for new users.
* **Acceptance Criteria:**

  * README.md clearly describes interactive-only usage.
  * Provides install guidance for `fzf`, `wl-clipboard` on Arch Linux.
  * Document size ≤ 200 lines.

---

### 📌 **200-005 · DOC · Create Minimal Man-page (`man1/prompts.1.scd`)**

* **Goal:** Provide minimal Unix-standard documentation.
* **Acceptance Criteria:**

  * Concise, ≤100 lines describing usage.
  * Matches README precisely.
  * Compiles cleanly with `scdoc`.

---

### 📌 **200-006 · INF · Add Development Automation (`Makefile`)**

* **Goal:** Provide essential automation tasks.
* **Acceptance Criteria:**

  * Targets: `make test`, `make clean`, `make setup`.
  * `make clean` removes all test/build artifacts.
  * `make test` executes full test suite successfully.

---

### 📌 **200-007 · INF · Repository Hygiene & Cleanup**

* **Goal:** Purge redundant files; finalize `.gitignore`.
* **Acceptance Criteria:**

  * Remove unused scripts.
  * Update `.gitignore` to exclude Python cache, editor artifacts, and build files (`__pycache__/`, `*.pyc`, `.ruff_cache`, etc.).

---

### 📌 **200-008 · INF · Restore AGENTS.md**

* **Goal:** Provide canonical audit-grade task ledger.
* **Acceptance Criteria:**

  * AGENTS.md clearly defines sprint goals, tasks, and acceptance criteria.
  * Reflects exactly the minimal requirements and approach.

---

### 📌 **200-009 · CI · Verify GitHub Actions Workflows**

* **Goal:** Confirm and simplify CI pipelines.
* **Acceptance Criteria:**

  * CI runs linting (`ruff`), shell checks (`shellcheck`), Python and shell tests.
  * Remove or adjust `release.yml` if Docker/SBOM not supported in minimal approach.

---

### 📌 **200-010 · ARC · Document Minimal Architecture Decision (ADR)**

* **Goal:** Clearly document minimalism and Wayland-only approach.
* **Acceptance Criteria:**

  * ADR (`docs/adr/minimal_wayland_only.md`) explains minimal slot-by-slot, fzf, wl-copy-only decisions.
  * Includes rationale and future implications.

---

## 📅 **Sprint Cadence Recommendation**

| Sprint | Targets                               | Tickets                            | Duration |
| ------ | ------------------------------------- | ---------------------------------- | -------- |
| 1      | Restore minimal CLI, slots, and tests | 200-001, 200-002, 200-003, 200-004 | 1 week   |
| 2      | Documentation, automation & cleanup   | 200-005, 200-006, 200-007, 200-008 | 1 week   |
| 3      | CI verification and ADR documentation | 200-009, 200-010                   | 1 week   |

---

## ✅ **Approval Rubric (Go/No-Go)**

| Area           | Threshold / Condition              | Verification              |
| -------------- | ---------------------------------- | ------------------------- |
| CLI Flow       | Only interactive slot-by-slot mode | Manual & automated tests  |
| Clipboard      | Only wl-copy supported             | Test verification         |
| Tests          | 95% coverage                       | pytest-cov, Bats coverage |
| Docs           | Clear, ≤200 lines README           | Doc review                |
| Infrastructure | Clean Makefile & .gitignore        | Repo hygiene checks       |

Any failing item results in a **no-go** for final release.

---

## 🌱 **Further Enhancements (Post-Release)**

After the minimal system is stable:

* **fzf preview pane** integration with syntax highlighting.
* **Optional Markdown plugin loading** (if community requests).
* **Sora/Hailuo direct API upload integration** (optional future feature).

---

## 📘 **Glossary**

| Term        | Definition                    |
| ----------- | ----------------------------- |
| **fzf**     | Command-line fuzzy finder     |
| **wl-copy** | Wayland clipboard utility     |
| **slot**    | Individual prompt category    |
| **Bats**    | Bash Automated Testing System |
| **ADR**     | Architecture Decision Record  |

---

## 🗂️ **Ticket YAML Stub (Example for GitHub issues)**

```yaml
id: 200-XXX
stream: SHE
title: Short Descriptive Ticket Title
dependencies: []
priority: P0
est_hours: 1
description: |
  Clearly describe the task and its scope in detail.
acceptance_criteria:
  - Bullet point measurable outcomes
deliverables:
  - List any files to update or create
  - Include documentation changes
notes: |
  Additional context or guidance
```

---

## 📑 **ADR Template (Architecture Decision Record)**

```markdown
# ADR-0001 – Minimal Slot-by-Slot Interactive Flow with Wayland-Only Clipboard

**Status:** Accepted
**Date:** YYYY-MM-DD

## Context
Prior iterations included complexity (plugins, cross-platform clipboards). Project goals emphasize minimalism, simplicity, and precise control.

## Decision
Implement a single interactive mode via fzf, slot-by-slot prompt creation defined solely by Python (promptlib.py). Support only Wayland clipboard (wl-copy).

## Consequences
- Simplicity: Easier maintenance and fewer edge-cases.
- Limited Compatibility: Only Arch Linux with Wayland supported initially.
- Future extension points remain clear and incremental.

## Alternatives Considered
- Multi-platform clipboard support (discarded for complexity).
- Plugin support via external files (deferred for future consideration).
