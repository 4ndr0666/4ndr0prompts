###############################################################################
# CODEX.md — WORK ORDER: Red-Team Prompt Mutation Toolkit ("4ndr0prompts")
# Repository Root: <repo>/          (branch: main)
#
# Sprint Scope: CANONICALIZATION, AGGREGATION, TEST, QA, API READINESS
# Objective: Achieve **verbatim, audit-grade aggregation** of all prompt data
#            (with all canonical misspellings) from dataset/rawdata.txt,
#            fully aligned to all APIs, slots, and category schemas.
#
# Audit Principle: RAWDATA IS CANON. Never "correct" spelling, structure, or
#                  content from rawdata.txt. Preserve all bypass techniques.
###############################################################################

## 0. Current State (2025-06-23)

**Directory tree**
```

.
├── 0-tests/
│   ├── CHANGELOG.md
│   ├── codex-generate.sh
│   └── codex-merge-clean.sh
├── AGENTS.md
├── CODEX.md                # <== THIS FILE
├── dataset/
│   ├── nsfwprompts.txt     # human-friendly, example dataset (not canonical)
│   ├── rawdata.txt         # CANONICAL dataset, all misspellings verbatim
│   ├── slots\_report.tsv    # (autogen) audit slot mapping
│   └── templates.json      # machine JSON for promptlib2.py etc.
├── prompt\_config.py        # config loader for JSON templates
├── promptlib2.py           # prompt generation (dataset-driven)
├── promptlib\_cli.py        # CLI interface
├── promptlib\_interactive.py# Python wrapper/fallback
├── promptlib.py            # legacy (DO NOT EDIT for Red Team)
├── promptlib\_tui.py        # TUI wrapper
├── prompts.sh
├── pyproject.toml
├── README.md
├── scripts/
│   └── parse\_rawdata.py    # canonical parser for dataset/rawdata.txt
└── tests/
├── test\_promptlib2.py
├── test\_promptlib.py
├── test\_promptlib\_tui.py
└── test\_rawdata\_parse.py

```

---

## 1. MANDATE: RAWDATA VERBATIM

- **rawdata.txt** is THE canonical input.  
  - *Never correct spelling, grammar, or idioms*: all bypasses, errors, and variants are essential for adversarial QA.
- **templates.json** and **slots_report.tsv** are regenerated strictly from rawdata.txt.
- **nsfwprompts.txt** is for demonstration only, not for generation or QA.

---

## 2. API STRUCTURE REQUIREMENTS

### [A] Categories and Slots

- Categories must be discovered and mapped *directly from* rawdata.txt using regex or logic (see scripts/parse_rawdata.py).
- Slots are aggregated per category via regex matching (see SLOT_PATTERNS in parse_rawdata.py).
- All canonical category and slot names must be preserved (even if derived via imperfect regex).

### [B] GET Endpoints (API Readiness)

- `GET /categories` returns all discovered categories (from templates.json).
- `GET /slots/<category>` returns all slots + slot-values for that category (from templates.json).
- All category and slot names must match those in templates.json.

---

## 3. WORK ORDER: Team Task Matrix

### [1] DATA PIPELINE CANONICALIZATION

- [ ] **Reparse** dataset/rawdata.txt using scripts/parse_rawdata.py with `--write`.
    - Ensure parse_rawdata.py has not been locally hacked to filter, correct, or "fix" content; must be pass-through.
    - Output must regenerate both templates.json and slots_report.tsv in-place.
    - Confirm all "misspelled" (bypass) data is present in all outputs.
    - Add new slot patterns if/when real bypass patterns appear (do NOT remove or alter existing ones unless correcting slot attribution, not data).

- [ ] **Commit and version-lock** any edits to parse_rawdata.py, templates.json, slots_report.tsv with meaningful commit messages.
    - Each commit must mention function count and line delta (see AGENTS.md).

### [2] AGGREGATION / COVERAGE AUDIT

- [ ] **Slot Coverage Audit:** scripts/parse_rawdata.py must extract ALL slot values (no omissions or false normalization).
    - Run `diff <(cat rawdata.txt) <(cat slots_report.tsv | cut -f3)` and report if any lines of rawdata.txt are missing from slot values.
    - Run pytest tests/test_rawdata_parse.py to ensure no placeholders, no missing categories, no API errors.

- [ ] **Category Integrity Check:**  
    - All categories in rawdata.txt must exist as keys in templates.json.
    - If a category is discovered in rawdata.txt that is missing from templates.json, halt and alert with an actionable error (never auto-add or silently ignore).
    - Document any unmatched/unclassifiable lines in an audit appendix.

- [ ] **Human Readability Report:**  
    - After generation, regenerate nsfwprompts.txt (or equivalent) for QA/UX, but mark it as non-canonical.

### [3] API + LIBRARY INTEGRATION

- [ ] **prompt_config.py**:  
    - Must use templates.json only (never static or hand-coded categories/slots).
    - Ensure promptlib2.py and all frontends (CLI, TUI, interactive) call the loader from prompt_config.py, not legacy promptlib.py.
    - Remove any deprecated or fallback category/slot sources in promptlib2.py.

- [ ] **promptlib2.py**:  
    - Must support random prompt generation using canonical templates and slots (see templates.json structure).
    - Expose programmatic `get_categories()` and `get_slots(category)` that reflect *all* canonical data.
    - Raise clear exceptions if categories or slots are missing or out-of-date.

- [ ] **Front-end Consistency:**  
    - CLI, TUI, and interactive must all surface canonical categories/slots from the loader.
    - All categories/slots shown to user must reflect rawdata.txt ground-truth.

- [ ] **API Documentation**:  
    - Document GET endpoints in README.md with real output examples.
    - All API docs must reference category/slot structure as parsed from rawdata.txt.

### [4] TESTING & CI

- [ ] **Test Coverage**:  
    - pytest must run test_rawdata_parse.py and all other relevant tests with coverage >= 90% on all critical modules.
    - All tests must pass with the current dataset, including edge-case data from rawdata.txt.

- [ ] **CI/CD Enforcement:**  
    - Add/expand a pre-commit config that enforces:
        - Black and ruff lint passes.
        - codex-merge-clean.sh is run on all .sh/.py files before commit.
        - No files with unresolved merge markers can be committed.
        - Slot/category audit passes.
        - All tests in tests/ must pass on commit and PR.

### [5] DOCUMENTATION & CHANGE MANAGEMENT

- [ ] **Changelog Discipline:**  
    - All changes, including new categories/slots or slot-mapping heuristics, must be listed in 0-tests/CHANGELOG.md.
    - All slot/category audits or exceptions must be noted in a block at the end of this CODEX.md.

- [ ] **README and AGENTS.md Update:**  
    - README.md must include an updated workflow showing the pipeline from rawdata.txt to API response.
    - AGENTS.md must reflect any new best practices or guardrails discovered during the sprint.
    - Ensure “no auto-correction” is called out as a security and research requirement.

---

## 4. CROSS-REFERENCE TABLE: KEY FILES

| File/Path                | Function                                       |
|--------------------------|------------------------------------------------|
| dataset/rawdata.txt      | CANONICAL PROMPT SOURCE — no corrections       |
| dataset/templates.json   | Machine-readable templates/slots for API/gen   |
| dataset/slots_report.tsv | Slot audit, autogenerated, for QA/review       |
| scripts/parse_rawdata.py | Canonical parser (slot, template aggregation)  |
| prompt_config.py         | Loader for templates.json                      |
| promptlib2.py            | Generator using canonical templates/slots      |
| promptlib_cli.py         | CLI (calls promptlib2 via prompt_config)       |
| promptlib_tui.py         | TUI frontend, must use canonical loader        |
| tests/                   | Unit and integration test suite                |

---

## 5. DELIVERABLES & AUDIT TRAIL

| ID | Deliverable                             | Acceptance Criteria                                    |
|----|-----------------------------------------|--------------------------------------------------------|
| D1 | templates.json and slots_report.tsv      | All verbatim, no normalized/corrected data             |
| D2 | GET /categories API                     | All categories reflect canonical rawdata.txt            |
| D3 | GET /slots/<category> API               | All slots/values per canonical mapping                  |
| D4 | promptlib2.py, prompt_config.py         | All logic references templates.json, not legacy/hand   |
| D5 | QA test suite                           | Full slot/category audit coverage; ≥90% test coverage  |
| D6 | README.md/AGENTS.md updated             | Workflows, guardrails, and security notes refreshed    |
| D7 | CHANGELOG.md                            | Full slot/category edits and exceptions documented      |

---

## 6. NONNEGOTIABLES & GUARDRAILS

- *No auto-correction of data, spelling, or structure. EVER.*  
- *All extracted slot/category data must remain audit-traceable to source (rawdata.txt, with line numbers if possible).*
- *No silent category/slot loss or fallback in user-facing APIs or CLI/TUI.*
- *All code and docs must note that this pipeline is for adversarial red-team research and does not represent production QA/Safety policy.*

---

## 7. AUDIT LOG / EXCEPTIONS (append as found)

> _Append any lines of rawdata.txt that could not be mapped, or other exceptions, here for team review._

---

# END CODEX.md
