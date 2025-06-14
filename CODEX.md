###############################################################################
# CODEX.md — Work-Order Playbook
# Project: Red-Team Prompt Mutation Toolkit
# Sprint: “Immediate Cleanup + Packaging + Prompts1 Aggregation”
# Scope EXCLUDES: Policy/Safety wiring · CI/CD · Docker / Demo UI
#
# Conventions
#   $   host-shell commands
#   >>> Python REPL snippets
#   #   explanatory comments
#
# Assumptions
#   • Git repository root is current working directory.
#   • Python ≥ 3.10 and make/grep/sed are available.
#   • Engineer works inside a fresh virtual-environment or container.
###############################################################################

## 0  Environment / Bootstrap

```bash
# 0-A — clone & branch
$ git clone <repo-url> redteam-prompts
$ cd redteam-prompts
$ git checkout -b feature/cleanup-packaging

# 0-B — toolchain
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -U pip wheel ruff black pytest pytest-cov python-slugify
````

> ✅ **Checkpoint**: `python -V` prints ≥ 3.10 and `ruff --version` prints a version.

---

## 1  Deliverable Matrix

| ID     | Deliverable                                                            | Key Acceptance Tests (Codex must enforce)                            |
| ------ | ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **D1** | Unified core **`promptlib_redteam.py`**; no `promptlib_interactive.py` | `python -c "import promptlib_redteam"` exits 0                       |
| **D2** | Runtime artefacts under **`var/`** only                                | Generating prompts populates `var/prompt_logs/` & `var/prompts_out/` |
| **D3** | **pytest** green, ≥ 85 % coverage                                      | `pytest -q && pytest --cov=promptlib_redteam -q` passes ≥ 85 %       |
| **D4** | Editable install via **`pyproject.toml`**                              | `pip install -e .` && `promptlib-rt --help` succeed                  |
| **D5** | **Plugin auto-loader** (YAML/Markdown)                                 | Dropping a plugin file enriches slots at runtime (unit test)         |
| **D6** | Updated **`README.md`** + generated **`docs/slot_catalogue.md`**       | `markdownlint` clean; links valid                                    |
| **D7** | **Prompts 1** corpus imported & reachable                              | Integrity test validates each prompt slug is generatable             |

Failure of any acceptance test must block merge.

---

## 2  Task-by-Task Execution Guide

### A  Core Canonicalisation

```bash
$ git mv promptlib_interactive.py promptlib_redteam.py
$ grep -RIl "promptlib_interactive" | while read f; do
      sed -i 's/promptlib_interactive/promptlib_redteam/g' "$f";
  done
$ python promptlib_cli.py --help || { echo "Import error"; exit 1; }
$ git add promptlib_redteam.py promptlib_cli.py promptlib_tui.py promptlib.sh category*/cat_template*.py
$ git rm promptlib_interactive.py
$ git commit -m "feat: canonicalise red-team core (rename interactive ⇒ promptlib_redteam)"
```

---

### B  Runtime Artefact Hygiene

```bash
$ mkdir -p var/prompt_logs var/prompts_out
$ echo "var/" >> .gitignore
```

Add to **`promptlib_redteam.py`** (top-level):

```python
from pathlib import Path
RUNTIME_DIR = Path(__file__).resolve().parent.parent / "var"
LOG_DIR     = RUNTIME_DIR / "prompt_logs"
OUTPUT_DIR  = RUNTIME_DIR / "prompts_out"
LOG_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
```

Refactor wrappers to use `OUTPUT_DIR`.
Generate two prompts → verify they land under `var/`.
Commit with message `refactor: route logs & outputs under var/`.

---

### C  Local Test Suite Skeleton

1. Create `tests/` with:

   * `test_slots.py` — assert every slot list is non-empty.
   * `test_generation.py` — generate 50 prompts per category, ensure no placeholders.
   * `test_cli.py` — `--dry-run` exits 0.

2. Run:

```bash
$ pytest -q && pytest --cov=promptlib_redteam -q
```

Commit: `test: baseline slot, generation, and CLI tests`.

---

### D  Editable Install & Console Scripts

Create **`pyproject.toml`** (PEP 621 example below ▷ adjust metadata):

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name            = "promptlib-redteam"
version         = "0.1.0"
description     = "NSFW filter stress-test prompt generator"
readme          = "README.md"
authors         = [{ name="Red-Team", email="security@example.com" }]
requires-python = ">=3.10"
dependencies    = ["prompt_toolkit>=3.0.43", "npyscreen>=4.10.5", "python-slugify>=8.0"]
license         = { text = "MIT" }

[project.scripts]
promptlib-rt     = "promptlib_cli:main"
promptlib-rt-tui = "promptlib_tui:main"
```

Test:

```bash
$ pip install -e .
$ promptlib-rt --help
```

Commit: `build: introduce pyproject.toml and console-scripts`.

---

### E  Plugin Auto-Loader

1. Create `promptlib_redteam/plugin.py` (see full code in Appendix A).
2. Add `plugins/` package and call `load_plugins()` in core `__init__.py`.
3. Unit-test dynamic enrichment (`tests/test_plugin_loader.py`).
4. Commit: `feat: pluggable slot loader with YAML/Markdown support`.

---

### F  Documentation

* `scripts/gen_catalogue.py` → writes `docs/slot_catalogue.md`.
* Expand README (dev install, plugin how-to, XDG paths).
* Run `markdownlint README.md docs/*.md`.
* Commit: `docs: expand README and auto-generate slot catalogue`.

---

### G  Prompts 1 Corpus Import

1. Move raw file → `data/prompts1_raw.txt`; add `data/*.txt export-ignore` to `.gitattributes`.
2. `scripts/import_prompts1.py` parses, dedupes, categorises lines, outputs `plugins/prompts1.yaml`.
3. Add integrity test (`tests/test_prompts1_integrity.py`) ensuring prompt slugs are reachable and raise coverage ≥ 85 %.
4. Commit: `feat: import Prompts 1 corpus into plugin system`.

---

## 3  Merge & Review Protocol

1. Run `./codex-merge-clean.sh $(git diff --name-only)` before every commit.
2. `pre-commit run --all-files` must pass — includes **shellcheck**, **shfmt**, **ruff**, **pytest**.
3. Pull-request body must list:

   * Tasks completed (A–G)
   * Coverage delta (`pytest-cov`)
   * Function & LOC counts for changed scripts
4. Reviewer checklist: D1–D7 ✅, coverage ≥ 85 %, no merge markers, `var/` ignored.

---

## 4  Coding Standards

* **Python** — auto-format with **black** (88 cols), lint with **ruff** (all fixes).
* **Shell**  — POSIX-sh, strict mode `set -euo pipefail`; pass **shellcheck -x** & **shfmt -i 2 -ci -sr**.
* Every script **must implement** `--help` and `--dry-run` if it mutates files.
* **No TODO/placeholder code** may remain in final PR.

---

## 5  Timeline (15 hours ≈ 2 days)

| Day | Morning     | Afternoon                          |
| --- | ----------- | ---------------------------------- |
| 1   | Tasks A + B | Task C (baseline tests)            |
| 2   | Task D + E  | Task F + G → raise coverage ≥ 85 % |

---

## 6  Failure Handling

If any acceptance test fails, Codex must:

1. Output failing command + stderr.
2. Abort pipeline with non-zero exit.
3. Leave PR in **Draft** state until green.

---

## 7  Post-Sprint (Out-of-Scope) Suggestions

* Wire policy/regex filter gates.
* Add GitHub Actions CI (ruff + pytest + coverage).
* Provide Dockerfile and Streamlit demo UI.

---

## Appendix A — Plugin Loader (reference implementation)

````python
# promptlib_redteam/plugin.py
from pathlib import Path
import yaml, re

SLOT_REGISTRY: dict[str, dict[str, list[str]]] = {}
PLUG_PAT = re.compile(r"\.(yml|yaml|md)$", re.I)

def merge_slot(cat: str, name: str, items: list[str]):
    dest = SLOT_REGISTRY.setdefault(cat, {}).setdefault(name, [])
    dest += [x for x in items if x not in dest]

def load_plugins(plugin_dir: Path):
    if not plugin_dir.exists():
        return
    for fp in plugin_dir.iterdir():
        if not PLUG_PAT.search(fp.name):
            continue
        txt = fp.read_text(encoding="utf-8")
        data = (yaml.safe_load(txt) if fp.suffix in {".yml", ".yaml"}
                else _extract_yaml_front_matter(txt))
        if not data:
            continue
        for cat, slots in data.items():
            for slot_name, items in slots.items():
                merge_slot(cat, slot_name, list(map(str.strip, items)))

def _extract_yaml_front_matter(md: str):
    import re, yaml
    m = re.search(r"```yaml(.*?)```", md, re.S | re.I)
    return yaml.safe_load(m.group(1)) if m else None
````

---


















