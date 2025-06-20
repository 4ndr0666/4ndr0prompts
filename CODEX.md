###############################################################################
# CODEX.md — Sprint “Raw-Data Canonicalisation v2”
# Repo: 4ndr0prompts | Branch: feature/raw-canonicalisation-v2
# Status: 🔴 OPEN (owner: @<your-initials>)
# Updated: 2025-06-19
#
# Mission
# ───────
# ◉ Elevate the raw-data pipeline so that *all* categories & slots in
#   `dataset/rawdata.txt` are captured, normalised, deduped and exported into a
#   deterministic `templates.json` — zero placeholders, no typos.
# ◉ Harden parser, tests and audit artifacts for CI and security review.
###############################################################################

## 0 ▪︎ Prerequisites
```bash
git checkout -b feature/raw-canonicalisation-v2
./0-tests/codex-merge-clean.sh $(git ls-files '*.py' '*.sh')
ruff --fix . && black .
pytest -q
````

> ✅ **Checkpoint:** tests green, no merge artifacts.

---

## 1 ▪︎ Deliverable Matrix

| ID | Deliverable / Path                       | Key Acceptance Tests                                  |
| -- | ---------------------------------------- | ----------------------------------------------------- |
| D1 | `scripts/parse_rawdata.py` (rev 2)       | 100 % slots deduped; handles FileNotFound; ≥90 % cov. |
| D2 | `dataset/templates.json` (regen)         | Contains **all 6 categories**, no placeholder tokens. |
| D3 | `dataset/slots_report.tsv` (regen)       | TSV ✓; values escaped; ≥1 row per slot value.         |
| D4 | `tests/test_rawdata_parse.py` (expanded) | ◻ no duplicates ◻ no empty slots ◻ all cats covered.  |
| D5 | `0-tests/CHANGELOG.md` (entry)           | Function & line counts + coverage delta.              |

---

## 2 ▪︎ Task Breakdown

### A. **Parser Hardening**

| Step | Action                                                                                                                         | File               | Owner |
| ---- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------ | ----- |
| A-1  | Add `try/except FileNotFoundError` in `_read_raw()` → exit 1 with msg                                                          | `parse_rawdata.py` |       |
| A-2  | Replace `list` accumulators with `set`, convert to sorted list at end                                                          | ″                  |       |
| A-3  | Escape `\t` and `\n` when writing `slots_report.tsv`                                                                           | ″                  |       |
| A-4  | Add `normalize(text:str)->str` (lowercase, ascii-fold, typo fix: `chek→cheek`, `brest→breast`) and run on every captured value | ″                  |       |
| A-5  | Expand `CATEGORY_RULES` & `SLOT_PATTERNS` per audit table below                                                                | ″                  |       |

#### 𝐒𝐋𝐎𝐓\_𝐏𝐀𝐓𝐓𝐄𝐑𝐍𝐒 additions

| Category                   | Slot             | Regex fragment   |               |          |             |           |      |         |
| -------------------------- | ---------------- | ---------------- | ------------- | -------- | ----------- | --------- | ---- | ------- |
| turning\_bending\_buttocks | CLOTHING\_BOTTOM | \`skirt          | pants         | trunks   | leggings?\` |           |      |         |
| turning\_bending\_buttocks | BUTTOCKS\_DESC   | \`round buttocks | bare buttocks | backside | thighs\`    |           |      |         |
| clothing\_chest\_exposure  | ACTION           | \`drool          | smack         | lean     | dance       | jiggle    | sway | grope\` |
| white\_fluid\_dripping     | LIQUID\_DESC     | \`pearly         | milky         | viscous  | ropey       | stringy\` |      |         |
| multi\_person\_interaction | INTERACTION      | \`kiss(?\:es)?   | touch         | caress   | stroke\`    |           |      |         |

*(extend as observed; update regex in code)*

---

### B. **Templates & Slot Generation**

| Step | Action                                                                                                                | Owner |
| ---- | --------------------------------------------------------------------------------------------------------------------- | ----- |
| B-1  | Implement `--trim-sentences N` flag (default 1) → keep first *N* sentences as template string.                        |       |
| B-2  | Ensure every category appearing in raw data has a **non-empty slot map** (create `{}` if no slots extracted).         |       |
| B-3  | Run `python scripts/parse_rawdata.py --write --trim-sentences 1` → regenerates `templates.json` & `slots_report.tsv`. |       |
| B-4  | Manually scan `slots_report.tsv` for obvious junk after first run; re-tune patterns if needed.                        |       |

---

### C. **Test Suite Expansion**

| Step | Action                                                                                                                             | File                          | Owner |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ----- |
| C-1  | Add `test_all_categories_accounted`, `test_no_empty_slot_lists`, `test_no_duplicate_slot_values` (see audit code)                  | `tests/test_rawdata_parse.py` |       |
| C-2  | Add TSV integrity test: open file after `--write` and `assert len(line.split('\t'))==3`.                                           | ″                             |       |
| C-3  | Update existing tests to call `parse_rawdata.py --write` inside tmp dir (use `tmp_path`) so artifacts are produced for assertions. | ″                             |       |

---

### D. **CHANGELOG & Documentation**

| Step | Action                                                                                                                                          | File                   | Owner |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ----- |
| D-1  | Append section under **Unreleased**: “Enhanced parser (7 funcs, 155 lines) … +3 tests, coverage +4 pp”                                          | `0-tests/CHANGELOG.md` |       |
| D-2  | In `README.md` → update *Usage* snippet: “Run `scripts/parse_rawdata.py --write --trim-sentences 1` after any update to `dataset/rawdata.txt`.” | `README.md`            |       |

---

### E. **Verification & Merge**

```bash
# After all code edits
ruff --fix .
black .
pytest -q --cov=.
./scripts/parse_rawdata.py --write --trim-sentences 1
bash 0-tests/codex-generate.sh        # should pass silently
git add -u
git commit -m "feat(parser): hardened rawdata canonicalisation (#A1-E2)"
```

PR body must include:

* Function/line counts for **parse\_rawdata.py**
* `pytest-cov` summary (before vs after)
* Sample diff of `templates.json` (old→new)

---

## 3 ▪︎ Audit Reference Tables (for dev use)

### 3.1 Missing Slot Coverage (pre-fix)

| Category                   | Slot  | Status         |
| -------------------------- | ----- | -------------- |
| multi\_person\_interaction | *ALL* | ❌ none present |
| white\_fluid\_dripping     | *ALL* | ❌ none present |
| other\_uncategorized       | *ALL* | ❌ none present |

### 3.2 Duplicate / Misspelt Values

| Value in TSV                                            | Normalised To                               |
| ------------------------------------------------------- | ------------------------------------------- |
| `tattoo of a black spade on her right bottom butt chek` | `tattoo of black spade on right butt cheek` |
| `tattoo of a black spade on her right butt chek`        | `tattoo of black spade on right butt cheek` |
| `tattoo` (generic)                                      | ***REMOVE*** (too generic)                  |

*(Normalisation implemented in `normalize()`)*

---

## 4 ▪︎ Acceptance Checklist (Reviewer)

* [ ] `dataset/templates.json` contains **6** categories, each template ≤1 sentence, no misspellings (`brest`→`breast` etc.).
* [ ] `dataset/slots_report.tsv` row-count ≥ distinct slot values, each line has 3 cols, no embedded tabs.
* [ ] `pytest -q` + coverage ≥ previous +4 pp.
* [ ] `ruff`, `black`, `shellcheck` all green (`pre-commit run --all-files`).
* [ ] No merge-artifact markers (`<<<<<<<`, `=======`, `>>>>>>>`) in repo (`git grep -nE '<<<<<<<|>>>>>>|======='` returns empty).
* [ ] CHANGELOG entry includes function/line metrics & coverage delta.

---

## 5 ▪︎ Timeline (ideal)

| Day       | Task IDs          | Hours     |
| --------- | ----------------- | --------- |
| D-0       | A-1 → A-3         | 2         |
| D-0       | A-4 → B-2         | 2         |
| D-1       | B-3 → B-4         | 1         |
| D-1       | C-1 → C-3         | 2         |
| D-1       | D-1 → D-2         | 0.5       |
| D-1       | Verification & PR | 1         |
| **Total** |                   | **6.5 h** |

---

*End of CODEX.md*
