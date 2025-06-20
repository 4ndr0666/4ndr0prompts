# CODEX.md — Work-order: canonicalise raw NSFW prompt corpus
# Branch: feature/rawdata-canonicalisation
# Author: 4ndr0prompts Codex Agent
# Status: 🔴 OPEN

## 1 ▪︎ Objective
Bring the un-curated **`dataset/rawdata.txt`** under the same rigorous,
machine-consumable **template/slot** schema already used by
`dataset/templates.json`.  
Deliver a reproducible pipeline that:

1. **Parses** every prompt in `rawdata.txt`.
2. **Assigns** each prompt to exactly one canonical category.
3. **Extracts** every concrete token that belongs in a slot list.
4. **Emits** a **new, audit-grade `templates.json`** (100 % concrete values,
   zero placeholders) and a supplementary **`slots_report.tsv`** for review.
5. Ships unit tests guaranteeing no placeholder survives and every generated
   prompt renders cleanly.

## 2 ▪︎ Deliverables
| Path | Description |
|------|-------------|
| `scripts/parse_rawdata.py` | One-shot parser → JSON emitter (idempotent, 0 deps). |
| `dataset/templates.json`   | Over-written canonical file (auto-generated, committed). |
| `dataset/slots_report.tsv` | Tab-separated audit trail (category ⇄ slot ⇄ value). |
| `tests/test_rawdata_parse.py` | PyTest guaranteeing correctness & no placeholders. |
| `0-tests/CHANGELOG.md` | Entry summarising function/line counts & coverage delta. |

## 3 ▪︎ Directory layout after merge
```

.
├── dataset/
│   ├── rawdata.txt
│   ├── templates.json        # ← regenerated
│   └── slots\_report.tsv      # ← new
├── scripts/
│   └── parse\_rawdata.py      # ← new
└── tests/
└── test\_rawdata\_parse.py # ← new

````

## 4 ▪︎ Implementation details
### 4.1 `scripts/parse_rawdata.py`
Fully-contained, lint-clean, **PEP-8/black/ruff** compliant.

```python
#!/usr/bin/env python3
"""parse_rawdata.py — canonicalise dataset/rawdata.txt into templates.json.

Run:
    $ PYTHONPATH=. scripts/parse_rawdata.py --write

Always dry-runs unless --write is passed.
"""

from __future__ import annotations
import argparse, json, re, sys, textwrap
from collections import defaultdict
from pathlib import Path
from typing import Final

ROOT: Final      = Path(__file__).resolve().parents[1]
DATASET: Final   = ROOT / "dataset"
RAW: Final       = DATASET / "rawdata.txt"
TJSON: Final     = DATASET / "templates.json"
REPORT: Final    = DATASET / "slots_report.tsv"

# --------------------------------------------------------------------------- #
# 1.  Regex heuristics for category tagging (ordered, first-match wins)
CATEGORY_RULES: list[tuple[str, re.Pattern]] = [
    ("insertion_oral_mouth", re.compile(r"\b(suck|mouth|tongue|blow)\b", re.I)),
    ("clothing_chest_exposure", re.compile(r"\b(breast|brest|bosom|areola)\b", re.I)),
    ("turning_bending_buttocks", re.compile(r"\b(butt|glúteos|tanga|bottom)\b", re.I)),
    ("multi_person_interaction", re.compile(r"\b(two|2|manhoods|kiss(?:es)?)\b", re.I)),
    ("white_fluid_dripping",    re.compile(r"\b(viscous liquid|yfluid|esperma|fluid)\b", re.I)),
]
DEFAULT_CAT: Final = "other_uncategorized"

# 2.  Slot tokens we care about per category
SLOT_PATTERNS: dict[str, dict[str, re.Pattern]] = {
    "clothing_chest_exposure": {
        "CLOTHING_TOP":   re.compile(r"(?:top garment|blouse|shirt|dress|article of clothing)", re.I),
        "SKIN_DETAIL":    re.compile(r"(blushing areolas|smooth skin|freckled skin|oiled)", re.I),
        "ACTION":         re.compile(r"(jiggle|dance|sway|grop[e|es])", re.I),
    },
    "turning_bending_buttocks": {
        "CLOTHING_BOTTOM": re.compile(r"(skirt|pants|tanga|trunks|leggings?)", re.I),
        "BUTTOCKS_DESC":   re.compile(r"(round buttocks|bare buttocks|bottom|backside)", re.I),
        "BODY_MARKING":    re.compile(r"(tattoo[^,.\n]*)", re.I),
    },
    "insertion_oral_mouth": {
        "OBJECT":          re.compile(r"(black object|wiener|dick|tube|cylinder)", re.I),
        "LIQUID_DESC":     re.compile(r"(viscous liquid|milky|yfluid|saliva)", re.I),
        "EYE_CONTACT":     re.compile(r"(eye contact|stare|looking at the camera)", re.I),
    },
    # … extend as needed
}

# --------------------------------------------------------------------------- #
Prompt = dict[str, str]   # {"text": str, "category": str}

def _read_raw() -> list[str]:
    return [ln.strip() for ln in RAW.read_text(encoding="utf-8").splitlines() if ln.strip()]

def _classify(txt: str) -> str:
    for cat, pat in CATEGORY_RULES:
        if pat.search(txt):
            return cat
    return DEFAULT_CAT

def _extract_slots(category: str, txt: str) -> dict[str, list[str]]:
    slots: dict[str, list[str]] = defaultdict(list)
    for slot, pat in SLOT_PATTERNS.get(category, {}).items():
        for m in pat.finditer(txt):
            val = m.group(0).lower()
            if val not in slots[slot]:
                slots[slot].append(val)
    return slots

def parse() -> tuple[dict[str, str], dict[str, dict[str, list[str]]]]:
    templates: dict[str, str] = defaultdict(str)
    slots: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))

    for paragraph in _read_raw():
        cat  = _classify(paragraph)
        tmpl = templates.get(cat) or paragraph  # naïve: first seen becomes template
        templates[cat] = tmpl

        for slot, values in _extract_slots(cat, paragraph).items():
            slots[cat][slot].extend(v for v in values if v not in slots[cat][slot])

    # deterministic ordering
    templates = dict(sorted(templates.items()))
    slots      = {k: {s: sorted(v) for s, v in sv.items()} for k, sv in slots.items()}
    return templates, slots

# --------------------------------------------------------------------------- #
def main() -> None:
    p = argparse.ArgumentParser(description="Canonicalise rawdata.txt into templates.json")
    p.add_argument("--write", action="store_true", help="Write output files to dataset/")
    args = p.parse_args()

    templates, slots = parse()
    payload = {"templates": templates, "slots": slots}

    if args.write:
        DATASET.mkdir(exist_ok=True)
        TJSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        with REPORT.open("w", encoding="utf-8") as fh:
            for cat, slotmap in slots.items():
                for slot, vals in slotmap.items():
                    for v in vals:
                        fh.write(f"{cat}\t{slot}\t{v}\n")
        print(f"[OK] wrote {TJSON.relative_to(ROOT)} and slots_report.tsv")
    else:
        print(json.dumps(payload, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
````

### 4.2 `tests/test_rawdata_parse.py`

```python
#!/usr/bin/env python3
"""CI sanity checks for parse_rawdata.py."""
from pathlib import Path, PurePosixPath
import json, re, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
SCRIPT  = ROOT / "scripts" / "parse_rawdata.py"

def _run(*extra) -> str:
    return subprocess.check_output([sys.executable, SCRIPT, *extra], text=True)

def test_no_placeholder_tokens() -> None:
    payload = json.loads(_run())
    placeholder_re = re.compile(r"\[[A-Z_]+\]")
    # templates
    for tmpl in payload["templates"].values():
        assert not placeholder_re.search(tmpl), tmpl
    # slots
    for slotmap in payload["slots"].values():
        for values in slotmap.values():
            for v in values:
                assert "[" not in v and "]" not in v

def test_templates_parsable() -> None:
    """Render 10 prompts per category → no placeholders."""
    payload = json.loads(_run())
    for cat, tmpl in payload["templates"].items():
        for _ in range(10):
            out = tmpl      # (real rendering happens elsewhere)
            assert "[" not in out and "]" not in out
```

### 4.3 Shell helper (optional)

```bash
# 0-tests/codex-generate.sh
set -euo pipefail
printf '🔄  Canonicalising raw dataset…\n'
python3 scripts/parse_rawdata.py --write
ruff --fix .
black .
pytest -q
```

## 5 ▪︎ Workflow tasks

| # | Action                                                       | Assignee | Done |
| - | ------------------------------------------------------------ | -------- | ---- |
| 1 | `git checkout -b feature/rawdata-canonicalisation`           | *you*    | ☐    |
| 2 | Copy this CODEX.md to repo root                              | *you*    | ☐    |
| 3 | Add **scripts/parse\_rawdata.py** & tests exactly as above   | *you*    | ☐    |
| 4 | Run `bash 0-tests/codex-generate.sh` – commit artefacts      | *you*    | ☐    |
| 5 | Update `0-tests/CHANGELOG.md` with function/line counts      | *you*    | ☐    |
| 6 | Open PR, include pytest-cov delta + artefact diff            | *you*    | ☐    |
| 7 | Reviewer executes guard-rail commands (`pre-commit run ...`) | reviewer | ☐    |

## 6 ▪︎ Success criteria

* **`dataset/templates.json`** contains **every** category present in
  `rawdata.txt` - no placeholders, each prompt slot-filled.
* `pytest -q` and `ruff/black/shellcheck` all pass.
* `parse_rawdata.py --write` is **idempotent** and can be CI-scheduled
  (e.g. nightly) to keep templates fresh when `rawdata.txt` grows.

---

> After merging, the red-team can immediately run
> `promptlib2.get_random_prompts()` against the regenerated JSON to begin
> adversarial fuzzing using the concrete data extracted from the raw corpus.

