###############################################################################
# CODEX.md — Work Order: Red-Team Prompt Mutation Toolkit (4ndr0prompts)
# Repository Root: <repo>   |   Branch: main or feature/automation-overhaul
# Status: OPEN, Living Document   |   Last Updated: 2025-06-23
#
# Mission Statement
# ─────────────────────────────────────────────────────────────────────────────
# Build a future-proof, fully-automated, audit-grade prompt generation and
# analysis toolkit for adversarial testing of NSFW filter boundaries. The 
# canonical source of all categories and slots is rawdata.txt. Human input and
# manual steps must be eliminated from all core workflows, including category/
# slot map maintenance, template re-generation, and coverage audits. Simplicity,
# security, and repeatability are paramount. 
###############################################################################

## I. Project Vision and Key Objectives

- **Simplicity:** All functionality must be accessible by invoking a single shell script: `./prompts.sh`.
- **Automation:** Eliminate manual steps in parsing, mapping, regenerating, and auditing; ensure all mappings and data structures are always up-to-date with `rawdata.txt` with zero human intervention.
- **Canonical Data Source:** `rawdata.txt` is the *sole* source of truth. Every file, map, and prompt must be traceable to, and only to, this dataset.
- **Self-Healing & Coverage:** The system should auto-correct or flag mismatches, automate category/slot extraction, and dynamically mitigate or reclassify uncategorized prompts.
- **Organizational Clarity:** Codebase should be periodically pruned for unused or redundant files and consolidated for maintainability without sacrificing test coverage.
- **Embedded Audit:** All integrity checks and coverage reports must be core to the single-run pipeline, not separate utilities.
- **Documentation & Review:** All workflows, outcomes, and exceptions must be thoroughly documented and easily auditable.

---

## II. Deliverables & Key Acceptance Tests

| ID | Deliverable / Path                 | Key Acceptance Criteria                               |
|----|------------------------------------|-------------------------------------------------------|
| D1 | `prompts.sh`                       | Single point-of-entry; runs parse, audit, test, regen |
| D2 | `parse_rawdata.py`                 | Zero manual flags; triggered by `prompts.sh` only     |
| D3 | `templates.json` & `slots_report.tsv` | 100% canonical; always match `rawdata.txt`           |
| D4 | In-code CATEGORY_MAP, slot lists   | Auto-extracted, always up-to-date                     |
| D5 | Unused/legacy scripts pruned       | No unused .py, .sh, or config after audit             |
| D6 | `audit_integrity` functionality    | Built-in: checks all category/slot coverage/mismatch  |
| D7 | `tests/` suite                     | Covers all core code; checks for all categories/slots |
| D8 | Updated `README.md`, `AGENTS.md`, `CHANGELOG.md` | Doc reflects new workflow, audit notes, exceptions    |

├── 0-tests
│   ├── CHANGELOG.md
│   ├── codex-generate.sh
│   └── codex-merge-clean.sh
├── AGENTS.md
├── CODEX.md
├── dataset
│   ├── nsfwprompts.txt
│   ├── rawdata.txt
│   └── templates.json
├── prompt_config.py
├── promptlib2.py
├── promptlib.py
├── prompts.sh
├── pyproject.toml
├── README.md
└── tests
    ├── test_promptlib2.py
    ├── test_promptlib.py
    ├── test_promptlib_tui.py
    └── ui
        ├── promptlib_cli.py
        ├── promptlib_interactive.py
        └── promptlib_tui.py

5 directories, 20 files

---

## III. Work Breakdown & Team Ticket Matrix

### 1. **SHELL AUTOMATION: `prompts.sh`**

| Task | Action | Owner | Ref. |
|------|--------|-------|------|
| S1-1 | Refactor `prompts.sh` to: <br> • Call `parse_rawdata.py` to auto-generate `templates.json` and `slots_report.tsv` if and only if `rawdata.txt` has changed or upon every run <br> • Run audit/integrity check as the next step <br> • Run pytest and show coverage <br> • Run ruff/black and codex-merge-clean.sh <br> • Print actionable summary/report <br> • Exit nonzero on any audit or test failure | Shell/Infra | D1, D2, D6 |
| S1-2 | Provide `--help` and `--dry-run` modes | Shell/Infra | D1 |
| S1-3 | Document all steps in script comments and in `README.md` | Shell/Infra | D8 |

---

### 2. **CORE PYTHON AUTOMATION**

| Task | Action | Owner | Ref. |
|------|--------|-------|------|
| P2-1 | Refactor `parse_rawdata.py`: <br> • Make it idempotent, non-interactive <br> • Remove any need for manual `--write`; run only as a subprocess from `prompts.sh` <br> • Accept `--force` to overwrite output even if unchanged | Py Team | D2 |
| P2-2 | Move/merge all CATEGORY_MAP and slot-list logic into one extraction function; source = `rawdata.txt` only | Py Team | D4 |
| P2-3 | Integrate normalization/audit for category/slot drift: <br> • Compare all categories and slots between dataset, code, templates.json, and slot report <br> • Print actionable mismatches <br> • Output full audit summary as part of pipeline | Py Team | D6 |
| P2-4 | Implement *self-healing* for uncategorized prompts: <br> • Attempt to re-categorize with updated patterns <br> • Fallback: auto-flag or move to `unresolved.tsv` for review <br> • Print clear report for QA | Py Team | D6 |

---

### 3. **CODEBASE CONSOLIDATION & PRUNING**

| Task | Action | Owner | Ref. |
|------|--------|-------|------|
| C3-1 | Inventory all .py and .sh scripts, libraries, and data files | Infra/Py Team | D5 |
| C3-2 | Deprecate and remove: <br> • Any module not called by `prompts.sh` or tests <br> • Legacy promptlib or slot mapping code (if replaced) <br> • Redundant dataset samples or unused configs | Infra/Py Team | D5 |
| C3-3 | Rename/refactor modules to clear, stable API names (e.g., consolidate all slot/category logic in one `prompt_agg.py`) | Infra/Py Team | D5, D4 |

---

### 4. **TESTING & AUDIT-DRIVEN QA**

| Task | Action | Owner | Ref. |
|------|--------|-------|------|
| T4-1 | Enhance tests/test_rawdata_parse.py and related tests: <br> • Test category/slot extraction on real, edge-case, and adversarial rawdata <br> • Fail if any prompt is dropped, re-mapped, or misspelling lost <br> • Verify “other_uncategorized” mitigation: number drops to 0 or prints actionable lines | QA | D7 |
| T4-2 | Add audit_integrity checks to test suite and as callable from `prompts.sh` <br> • Print summary at end of run (missing/extra categories, slot mismatches, slotless prompts, uncategorized lines) <br> • Provide human-parseable log file | QA | D6 |
| T4-3 | Run full pytest, coverage, linter suite in shell script <br> • All must pass for “success” exit | QA | D7 |

---

### 5. **DOCUMENTATION & CHANGE MANAGEMENT**

| Task | Action | Owner | Ref. |
|------|--------|-------|------|
| D5-1 | Update `README.md` with: <br> • Overview of canonical, automated pipeline <br> • Example run: `./prompts.sh` <br> • Explanation of “verbatim, adversarial data preservation” and audit philosophy <br> • How to review unresolved prompts | Docs | D8 |
| D5-2 | Update `AGENTS.md` and inline code comments to reflect new automation, guardrails, and self-healing/audit design | Docs | D8 |
| D5-3 | Log all changes, slot pattern extensions, and audit outcomes in `0-tests/CHANGELOG.md` <br> • Include function count, line delta, and coverage stats | Docs | D8 |

---

## IV. Acceptance Criteria & Final Audit Checklist

- [ ] **prompts.sh** runs all steps, prints audit summary, and exits 0 only if all categories, slots, and templates are in sync and all tests/linting pass.
- [ ] **No manual CATEGORY_MAP or slot mapping** in any module; all mappings/logic sourced from rawdata.txt via parser/aggregator.
- [ ] **No “other_uncategorized” prompts** remain (or all unresolved lines are printed/audited at run’s end).
- [ ] **All legacy/unreferenced scripts are pruned** or marked for deletion in the next sprint.
- [ ] **Slot/category drift and test coverage are reported** at every run (stdout and human-readable log).
- [ ] **README, AGENTS.md, and CHANGELOG.md** are all updated, matching the living state of the codebase.
- [ ] **Rawdata tokens (misspellings, obfuscation, bypasses)** are preserved verbatim throughout the pipeline and into all downstream outputs.

---

## V. Further Enhancements: Roadmap & Open Questions

### A. **Dynamic Slot Pattern Learning**
- Integrate ML/NLP to auto-suggest new slot regexes from previously uncategorized prompts.
- Allow admin to accept/reject suggested patterns for future runs.

### B. **API/Service Integration**
- Add a web API layer (e.g. FastAPI) for GET /categories, GET /slots/<category>, and POST prompt preview.

### C. **Role-Based Workflow**
- Build interactive TUI/CLI for red team ops that displays slot/category drift in real time.

### D. **Advanced Logging & Analytics**
- Add time-series and usage metrics for audit and trending (which attack vectors bypass the most?).

### E. **Automated Reclassification**
- If patterns are updated or extended, automatically reprocess unresolved prompts and surface any that finally resolve as success stories.

### F. **Adversarial Pattern Tracking**
- Track and report on which slot values or category triggers most frequently bypass security filters.

### G. **Plug-in Expansion**
- Allow third-party pattern plug-ins or category/tag classifiers for community red-team research.

---

## VI. Living Document Policy

- This work order and all referenced audit trails are to be updated after each meaningful change to the data pipeline, pattern logic, or automation script. All changes should be timestamped, author-attributed, and clearly referenced in CHANGELOG.md.
- Any exceptions, failed audits, or reclassification issues must be appended to the bottom of this CODEX.md as an audit log, with full reproduction instructions.

---

## VII. Summary

This work order captures all actionable, delegated steps for a **fully-automated, future-proof, self-healing red-team prompt mutation system**, in which the canonical dataset (`rawdata.txt`) is always source of truth and all logic, mapping, and audit reporting adapts automatically. Every component (parsing, mapping, audit, test, and report) is chained through a single shell script and produces a living, verifiable trail of all transformations and exceptions for ongoing adversarial research and testing.

---
# END OF WORK ORDER
