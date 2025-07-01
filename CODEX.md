###############################################################################
# RELEASE CODEX.md — Final Production Release Work Order: 4ndr0prompts
# Repository Root: <repo-root>     |     Branch: main (Release Candidate)
# Version: 1.0.0-rc     |     Status: 🚦 IN PROGRESS (Hand-off to DEV)
# Prepared: 2025-06-24  |     Author: Project Automation/QA
###############################################################################

## I. OVERVIEW & OBJECTIVE

This document constitutes the definitive, audit-grade, cross-functional work order and automation directive for the final consolidation, release, and QA of the 4ndr0prompts Red Team Prompt Mutation Toolkit.  
**It is intended for direct handoff to the dev and QA team, requiring zero ambiguity and total automation. All tasks are categorized as work tickets, with required criteria, audit mechanisms, and academic-level documentation.**  
All infrastructure and code changes must uphold best practices for production software engineering, and every section of this document is a required deliverable for a successful, maintainable release.

---

## II. RELEASE MANIFEST & CRITERIA

- **Release Goal:** Deliver a single, automated, prompt mutation pipeline with only one user-facing interface (`prompt_toolkit`), entrypointed via `prompts.sh`, driven solely by `rawdata.txt`, producing fully random, reproducible, adversarial prompts for red team hardening.
- **Codebase must be:**  
  - **Self-healing:** Auto-regenerates `templates.json` and slot structures on every run.
  - **Minimal:** Only one UI, one business logic hub, one config loader.
  - **Audit-grade:** All critical actions, code changes, and automation steps are logged, checked, and cross-referenced.
  - **Fully-automated:** No human-in-the-loop for aggregation, category/slot mapping, or QA.  
  - **Well-documented:** All logic, methods, and hand-offs are explicit, versioned, and cross-team ready.
  - **No cyclomatic complexity or ambiguity:** All code must be modular, testable, and predictable.

---

## III. WORK TICKET BREAKDOWN

### A. **INFRASTRUCTURE & ENTRYPOINT (prompts.sh)**

**Ticket A1: Entrypoint Hardening**
- Refactor `prompts.sh` to:
  - **Always call** `python3 scripts/parse_rawdata.py --write` (idempotent generation of templates/slots).
  - **Auto-launch** the canonical promptlib interface (`prompt_toolkit` UI, formerly `promptlib_cli.py`, now `promptlib.py`).
  - **Check for** the existence and freshness of `rawdata.txt` and `templates.json` before launching UI.  
  - **Validate** output and exit status for each subprocess.  
  - **ShellCheck compliance** (run `shellcheck -x prompts.sh`), all paths explicit.
  - **Remove all UI mode switches** (e.g., `--interactive`, `--cli`, `--tui`). No ambiguity.

**Ticket A2: Automation and Logging**
- Automate logging of:
  - All code generation and QA steps (with timestamps, exit codes, and error output).
  - All template regeneration and slot auditing.
- Logs to be written under `${XDG_DATA_HOME}/4ndr0prompts/logs/` and appended to `0-tests/CHANGELOG.md`.

---

### B. **CODEBASE CONSOLIDATION & MODULE MERGE**

**Ticket B1: Unified Prompt Logic**
- Merge all viable prompt aggregation, slot/category logic from `promptlib2.py` into the new canonical `promptlib.py`.
- Remove (`git rm`) all duplicate, deprecated, or unused files:
  - `promptlib2.py`, `promptlib_tui.py`, `promptlib_interactive.py`, `/ui` directory, and related pycache.
- Update all references (tests, scripts, entrypoints) to only use `promptlib.py`.

**Ticket B2: Refactor promptlib.py for Sole Ownership**
- Restructure `promptlib.py` to:
  - Expose a single `main()` entrypoint for interactive use, importing business logic from within.
  - Use only `prompt_toolkit` for all user input/output and randomization.
  - Import slot/category info dynamically from `prompt_config.py`.
  - Be idempotent and locally scoped (no arbitrary globals).
- Lint, test, and document every function.  
- **Line count and function count to be logged before and after refactor.**

---

### C. **CONFIGURATION LOADER & DATA PIPELINE**

**Ticket C1: Canonical Config Loader (`prompt_config.py`)**
- `prompt_config.py` must:
  - Load only from the canonical `templates.json`.
  - Provide API for categories/slots with explicit error handling.
  - Expose all paths and imports at the top, no in-function imports.
  - Separate variable declarations from assignments, with explicit types.

**Ticket C2: Automation of Data Aggregation (`parse_rawdata.py`)**
- `parse_rawdata.py` must:
  - Always run on every `prompts.sh` execution (or if `rawdata.txt` is newer than `templates.json`).
  - Aggregate all slot/category data verbatim, with no normalization or typo correction.
  - Write deterministic, audit-safe `templates.json` and slot mapping.
  - Lint and test every function for logic, parsing, and output accuracy.

---

### D. **TESTING, LINTING, & QA**

**Ticket D1: Test Suite Hardening**
- All test modules (`tests/`) must:
  - Cover every function in `promptlib.py`, `prompt_config.py`, and `parse_rawdata.py`.
  - Confirm that every category/slot is present and correctly mapped.
  - Explicitly fail on placeholder tokens, empty slot lists, or unclassified prompts.
  - Pass under both Python 3.10+ and shell environments (Arch, ZSH).

**Ticket D2: Lint, Type, and Security Checks**
- Run and enforce:
  - `black .`
  - `ruff .`
  - `shellcheck -x prompts.sh`
  - `mypy promptlib.py prompt_config.py`
  - Security scans for all scripts (e.g., `bandit -r .`)
- All failures must be resolved, and logs submitted as part of release audit.

**Ticket D3: Automation and Reporting**
- Automate reporting (markdown and plaintext logs) for:
  - Line count, function count, and coverage for each module before/after release.
  - Audit log of all slot/category changes since last baseline.
  - Full error/output logs for each test and automation step, saved under logs.

---

### E. **DOCUMENTATION & RELEASE QA**

**Ticket E1: Documentation Audit**
- Update all project documentation (`README.md`, `AGENTS.md`, `CODEX.md`) to:
  - Describe the unified UX/logic and new automation process.
  - Reference only canonical modules and entrypoints.
  - Provide a single run example: `./prompts.sh`.
  - Explain the self-healing, audit-grade, automated pipeline.
  - Explicitly note all deprecated modules, with migration notes if needed.

**Ticket E2: Release Checklist and Rubric**
- Before marking as “release ready”, confirm that:
  - All automation tasks are completed and logs present.
  - All code meets criteria and rubric in the initial directive.
  - Function/line counts match expected output, with no untracked increases/decreases.
  - No legacy UI code, unused configs, or ambiguous entrypoints remain.
  - A final “release candidate” tag is added to the repo, with CHANGELOG updated.

---

### F. **FUTURE ENHANCEMENTS ROADMAP (For Team Handover)**

| TID | Enhancement                          | Description                                                    |
|-----|--------------------------------------|----------------------------------------------------------------|
| F1  | Real-time Slot Pattern Learning      | Integrate ML/NLP for auto-suggesting new slot patterns         |
| F2  | Web API Layer                        | RESTful interface for remote prompt gen/audit                  |
| F3  | Batch/Plugin System                  | YAML/MD plugin loaders for prompt/slot expansion               |
| F4  | Prompt Audit Dashboard               | Web UI or CLI dashboard for audit trails and category usage    |
| F5  | Security Integration                 | Real-time policy/regex filters pre-output                      |
| F6  | Team/Role Workflows                  | User/account-based access for prompt building/testing          |
| F7  | CI/CD with Deployment Automation     | Fully automated CI/CD for all core workflows                   |

---

## IV. QA/AUDIT TABLE & CROSS-REFERENCE

| Ticket | Module/File         | Action                      | QA/Audit Required        | Status  |
|--------|---------------------|-----------------------------|--------------------------|---------|
| A1     | prompts.sh          | Entrypoint & Automation     | ShellCheck, logs, test   |         |
| B1,B2  | promptlib.py        | Merge, Refactor             | Lint, test, doc, count   |         |
| C1     | prompt_config.py    | Loader Validation           | mypy, test, doc          |         |
| C2     | parse_rawdata.py    | Aggregator Automation       | test, count, audit log   |         |
| D1     | tests/              | Unit & Integration          | pytest, log, audit       |         |
| D2     | ALL                 | Lint/Type/Security Checks   | black, ruff, shellcheck  |         |
| D3     | logs/0-tests/CHANGELOG | Audit Trail              | Review, tag, log         |         |
| E1     | README, AGENTS, CODEX | Docs Update               | Review, clear paths      |         |
| E2     | Repo root           | Release Finalization        | Tag, cross-team signoff  |         |

---

## V. CRITERIA, RUBRIC, AND FINAL ACCEPTANCE

**Release is approved only if all of the following are met:**
- One canonical entrypoint (`prompts.sh`), one UX (`promptlib.py`), one config (`prompt_config.py`), one data parser (`parse_rawdata.py`).
- No legacy UI, TUI, fallback, or redundant scripts remain.
- All code, docs, and logs are linted, tested, security checked, and up-to-date.
- All actual values are declared and assigned correctly; no unbound or ambiguous variables.
- Every automation action is logged and traceable.
- All variable declarations, error handling, exports, and paths follow best practices and comply with Arch and ZSH.
- Automation eliminates human error or drift; all future contributions must pass this standard.

---

## VI. SEGMENTED EXECUTION PLAN

If work output exceeds platform constraints, segment work by:
- Module (A, B, C, D, E)
- Output logs per segment, in markdown code blocks
- Notify team when additional output is required
- Never truncate logic or output; always note segment boundary and continuation.

---

## VII. FINAL DELIVERY & HAND-OFF

- Once all tickets are complete, the repo is tagged `v1.0.0-rc`.
- `CHANGELOG.md` and release audit are submitted for signoff.
- This document is archived as the canonical work order and QA reference.
- **No further work or refactoring is permitted until QA signoff is received.**

---

**End of CODEX.md (Release Work Order)**
