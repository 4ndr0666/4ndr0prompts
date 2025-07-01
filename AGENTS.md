# AGENTS.md — 4ndr0prompts (Production Release)
# Repository Root: <repo-root>/      (branch: main)
#
# Purpose
# ───────
# This repository delivers the Red-Team Prompt Mutation Toolkit, 4ndr0prompts:
# a minimal, Python-driven, **prompt_toolkit-only** interactive application for generating adversarial prompts that probe and harden NSFW filter boundaries. 
# This release embodies *total automation*, *single-source UX*, and *audit-grade reproducibility* as codified in the CODEX.md work order.

---

## Directory Summary (Release Structure)
```

├── 0-tests/
│   ├── codex-generate.sh        # Automated build/test/QA pipeline
│   └── codex-merge-clean.sh     # Merge artifact scrubber (pre-commit hook)
├── AGENTS.md                    # General automation & policy directives (this file)
├── CODEX.md                     # Release work order (audit-traceable)
├── dataset/
│   ├── nsfwprompts.txt          # Human-auditable prompt corpus (not canonical)
│   ├── rawdata.txt              # Canonical prompt corpus (adversarial, verbatim)
│   ├── slots\_report.tsv         # Auto-generated audit log: slots & values
│   └── templates.json           # Canonical template/slot config (auto-generated)
├── prompt\_config.py             # Canonical loader for templates.json
├── promptlib.py                 # Unified prompt\_toolkit UI and logic (SOLE INTERFACE)
├── prompts.sh                   # Only entrypoint; orchestrates automation & UX
├── scripts/
│   └── parse\_rawdata.py         # Canonical dataset parser (auto-run by prompts.sh)
├── pyproject.toml               # Linting, test, and build config
├── README.md                    # End-user/project overview & workflow
└── tests/
├── conftest.py
├── test\_promptlib.py
├── test\_rawdata\_parse.py
└── ...

```

---

## Configuration & Automation
- All prompt templates and slots must originate from `dataset/rawdata.txt`, aggregated and structured by `scripts/parse_rawdata.py`, and loaded from `dataset/templates.json`.
- **No manual edits** are permitted to templates.json or slot/category maps; all changes must flow through the parser and automation.
- The only permitted user interface is via `prompt_toolkit` as implemented in `promptlib.py`, launched exclusively by `prompts.sh`.
- All automation and code quality steps are orchestrated in `prompts.sh` and `0-tests/codex-generate.sh`.

---

## General Engineering & Contribution Best Practices

- **Eliminate manual toil:** Every recurring engineering or QA task must be automated; contributors must *not* be relied on for routine aggregation, mapping, or regeneration.
- **No placeholders, partial stubs, or incomplete code paths** are permitted.
- **Full code coverage and linting** are enforced at every stage (ruff, black, shellcheck, mypy, bandit, pytest).
- **Absolute path and import clarity**—all file and module references must be explicit, never implicit.
- **Strict error handling and explicit validation** on all function calls and external process invocations.
- **Enforce idempotency:** All scripts and entrypoints must be safe to run repeatedly.
- **Minimize complexity:** No legacy, fallback, or multi-path logic is permitted in released code.

---

## Workflow and Automation Policy

- The only user entrypoint is:
```

./prompts.sh

```
This script must:
1. **Run all pre-flight automation** (parse, audit, test, lint).
2. **Auto-generate templates/slots** from rawdata.txt via parse_rawdata.py.
3. **Launch promptlib.py** for interactive, random prompt exploration and export.
- All slot/category and prompt mappings must always reflect the canonical, audit-traceable structure defined by rawdata.txt and verified by scripts/parse_rawdata.py.
- All output logs, audit records, and error traces are written under `${XDG_DATA_HOME}/4ndr0prompts/logs/` or `0-tests/`.

---

## Coding & Linting Standards

- Use `printf` (not `echo`) for portability.
- Validate all shell variable exports and command return codes.
- Use POSIX-sh, `set -euo pipefail`, and pass ShellCheck.
- Prefer explicit over implicit: all variables, imports, and assignments must be declared and assigned on separate lines.
- No `&>`; use `>file 2>&1` for redirection.
- All functions must be locally scoped, idempotent, and free from side effects unless otherwise documented.
- No cyclomatic complexity or ambiguous code paths are permitted; all decision trees must be visualized (e.g., PlantUML) and documented in PRs as needed.

---

## Test, Lint, and Review Protocol

- All tests must be defined under `tests/`, use pytest (with coverage reporting), and cover all canonical functions and logic paths.
- Run full lint, type, and security checks on every PR and before every release candidate:
- `black .`
- `ruff .`
- `shellcheck -x prompts.sh`
- `mypy promptlib.py prompt_config.py`
- `bandit -r .`
- Use `0-tests/codex-merge-clean.sh` on every committed/modified file.
- PRs must disclose function and line count for every revised module, and report the change delta.

---

## Authorization and Audit Guardrails

- Contributors are authorized to modify only those files explicitly named in the current work order or CODEX.md.
- No bypassing of lint, dry-run, or coverage requirements is permitted without written, documented exception in AGENTS.md and CODEX.md.
- All audit trails (logs, changelogs, error output, and diffs) must be preserved for review.
- Final release or tag must be signed off by the QA/Automation lead and documented in CHANGELOG.md and README.md.

---

## XDG Compliance

- Config:  `${XDG_CONFIG_HOME:-$HOME/.config}/4ndr0prompts/`
- Data:    `${XDG_DATA_HOME:-$HOME/.local/share}/4ndr0prompts/`
- Cache:   `${XDG_CACHE_HOME:-$HOME/.cache}/4ndr0prompts/`
- Logs:    `${XDG_DATA_HOME:-$HOME/.local/share}/4ndr0prompts/logs/`

---

## Required Tests (Minimum)

1. All slot lists non-empty and de-duplicated.
2. 50 random prompts per category, no placeholders.
3. Promptlib main() always returns exit 0 on completion.
4. Templates and slots must always match dataset/rawdata.txt via audit.
5. Codebase passes all linters, shellcheck, and static analysis.
6. All output artifacts are reproducible and audit-traceable.

---

## Merge & Review Protocol

1. PRs must include function count, line count, and test/lint logs.
2. Reviewer must run:
 - `pre-commit run --all-files`
 - `./0-tests/codex-merge-clean.sh $(git diff --name-only main..HEAD)`
 - `pytest --cov`
3. Any unreviewed merge artifact or failed QA is grounds for rejection.
4. All changes and QA outcomes are logged to CHANGELOG.md and 0-tests/task_outcome.md.

---

## Finalization

- **No further releases or changes may be made without a revision to AGENTS.md and CODEX.md and sign-off from the release manager.**
- Any exceptions, failed audits, or unclassified prompts must be appended to the end of AGENTS.md as an audit log with full reproduction instructions.

---

**End of AGENTS.md (Production Release)**
