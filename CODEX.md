###############################################################################
# CODEX.md — Sprint “Raw-Data Canonicalisation v2”
# Repo: 4ndr0prompts | Branch: feature/raw-canonicalisation-v2
# Status: 🔴 OPEN | Owner (@<you>)
# Updated: 2025-06-19
#
# Mission
# ───────
# Convert **dataset/rawdata.txt** into a fully machine-readable, verbatim
# template + slot schema while **preserving every original token exactly as it
# appears in the raw corpus**.
# No placeholders, no editorial “fixes” or spell-corrections—misspellings that
# helped bypass filters are *valuable signal* and **must remain untouched**.
###############################################################################

## 0 ▪︎ Prerequisites
```bash
git checkout -b feature/raw-canonicalisation-v2
./0-tests/codex-merge-clean.sh $(git ls-files '*.py' '*.sh')
ruff --fix . && black .
pytest -q
````

---

## 1 ▪︎ Project Files & Deliverable Matrix

| ID     | Output / Path                            | Acceptance Tests                                   |
| ------ | ---------------------------------------- | -------------------------------------------------- |
| **D1** | `dataset/rawdata.txt` (rev 2)            | ≥ 90 % cov. 0 typos *added*, exact raw tokens kept |
| **D2** | `dataset/templates.json` (regen)         | 6 categories, ≤1 sentence each, verbatim text      |
| **D3** | `dataset/nsfwprompts.txt` (regen)        | Each row = category⇄slot⇄value, raw spelling kept  |
| **D4** | `tests/` `tests/ui` (expanded)           | ✔ no placeholders ✔ no **identical** duplicates    |
| **D5** | `0-tests/CHANGELOG.md`                   | Function+line counts & coverage delta              |

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

## 2 ▪︎ Task Breakdown

### A · Parser Hardening (verbatim mode)

| Step    | Action                                                                                                                       | File               |
| ------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| **A-1** | Wrap `_read_raw()` in `try/except FileNotFoundError` → exit 1 with msg                                                       | `parse_rawdata.py` |
| **A-2** | Replace list → set for slot accumulation, convert to **sorted list** (keeps unique *identical* tokens, retains misspellings) | ″                  |
| **A-3** | Escape tab/ newline when writing `slots_report.tsv` (`v.replace('\t','\\t').replace('\n',' ')`)                              | ″                  |
| **A-4** | Remove previous “normalise typo” idea; *do not* alter spelling.                                                              | ″                  |
| **A-5** | Expand `CATEGORY_RULES` & `SLOT_PATTERNS` (table §3) to capture all tokens now observed                                      | ″                  |

### B · Template & Slot Generation

| Step    | Action                                                                                                   |
| ------- | -------------------------------------------------------------------------------------------------------- |
| **B-1** | Add `--trim-sentences N` flag (default 1) → keep first *N* sentences ***unchanged*** as template string. |
| **B-2** | Ensure **every** detected category has at least an empty slot dict in output.                            |
| **B-3** | Run `python scripts/parse_rawdata.py --write --trim-sentences 1` to regenerate JSON + TSV.               |
| **B-4** | Quick human scan of TSV: ensure no placeholder tokens remain (`[SLOT]`).                                 |

### C · Test-Suite Expansion

| Step    | Action                                                                                                                        | File                          |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| **C-1** | Add: `test_all_categories_accounted`, `test_no_empty_slot_lists`, `test_no_duplicate_slot_values` (identical duplicates only) | `tests/test_rawdata_parse.py` |
| **C-2** | TSV integrity test: `assert len(line.split('\t')) == 3` for every row after `--write`.                                        | ″                             |
| **C-3** | Update existing tests to call script with `--write` inside `tmp_path` sandbox.                                                | ″                             |

### D · CHANGELOG + Docs

| Step    | Action                                                                                                                       |                        |
| ------- | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| **D-1** | Append entry under **Unreleased** detailing:<br>• parse\_rawdata.py now 7 funcs / \~155 lines<br>• +3 tests / coverage +4 pp | `0-tests/CHANGELOG.md` |
| **D-2** | `README.md` → update usage snippet showing new flag & workflow.                                                              |                        |

### E · Verification & PR

```bash
ruff --fix .
black .
pytest -q --cov=.
./scripts/parse_rawdata.py --write --trim-sentences 1
bash 0-tests/codex-generate.sh        # should pass
git add -u
git commit -m "feat(parser): verbatim rawdata canonicalisation (#A1-E2)"
```

PR body **must include**:

* Function/line metrics for new parser revision
* `pytest-cov` delta
* Diff of `templates.json` (old → new)

---

## 3 ▪︎ Slot-Pattern Additions (§A-5)

| Category                   | Slot             | Regex snippet (verbatim capture) |               |         |           |          |           |         |
| -------------------------- | ---------------- | -------------------------------- | ------------- | ------- | --------- | -------- | --------- | ------- |
| turning\_bending\_buttocks | CLOTHING\_BOTTOM | \`skirt                          | pants         | trunks  | leggings? | tanga\`  |           |         |
| turning\_bending\_buttocks | BUTTOCKS\_DESC   | \`round buttocks                 | bare buttocks | bottom  | backside  | thighs\` |           |         |
| clothing\_chest\_exposure  | ACTION           | \`drool                          | smack         | lean    | dance     | jiggle   | sway      | grope\` |
| white\_fluid\_dripping     | LIQUID\_DESC     | \`pearly                         | milky         | viscous | ropey     | stringy  | yfluid\`  |         |
| multi\_person\_interaction | INTERACTION      | \`kiss(?\:es)?                   | touch         | caress  | stroke    | hold     | embrace\` |         |

> **Important:** *Leave spelling exactly as matched in raw text.*
> Regex should therefore capture variants like `"brests"` if present.

---

## 4 ▪︎ Acceptance Checklist (Reviewer)

* [ ] `dataset/templates.json` has 6 categories; each template ≤1 sentence, matches raw wording verbatim.
* [ ] `dataset/slots_report.tsv` exists; every line has 3 fields, tokens verbatim, no tabs in values.
* [ ] No placeholder brackets in either file.
* [ ] Pytest green; coverage ≥ previous +4 pp.
* [ ] `ruff`, `black`, `shellcheck`, `pre-commit run --all-files` clean.
* [ ] No merge-artifact markers in repo (`git grep -nE '<<<<<<<|>>>>>>|======='`).
* [ ] CHANGELOG updated with metrics.

---

## 5 ▪︎ Timeline (ideal)

| Day       | Tasks     | Effort    |
| --------- | --------- | --------- |
| D-0 AM    | A-1 → A-3 | 2 h       |
| D-0 PM    | A-4 → B-2 | 2 h       |
| D-1 AM    | B-3 → B-4 | 1 h       |
| D-1 AM    | C-1 → C-3 | 2 h       |
| D-1 PM    | D-1 → E   | 1.5 h     |
| **Total** |           | **8.5 h** |

---

### Footnote

Misspellings in raw data (e.g., “brests”, “chek”) are *intentional adversarial payloads* and **must be kept verbatim**.
All deduplication is **value-exact only**; phrasal near-duplicates remain distinct.

*End of CODEX.md*
