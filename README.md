# 4ndr0prompts

This repository contains utilities for generating and testing red-team prompt mutations. Development follows strict linting and testing rules.

## Setup

1. Install the development dependencies:
   ```bash
   pip install pre-commit ruff black pytest shellcheck
   ```
2. Install the pre-commit hooks:
   ```bash
   pre-commit install
   ```
3. The hooks run `0-tests/codex-merge-clean.sh` first and then execute
   **ruff**, **black**, **shellcheck**, and **pytest** on changed files.

## Development Workflow

- All code changes must pass **ruff**, **black**, **pytest**, and the merge-artifact scrubber `0-tests/codex-merge-clean.sh`.
- The hooks run automatically via pre-commit and should also run in CI for every pull request that modifies code files.
- Documentation-only updates can skip these checks, but mixed changes run the full suite.

Run all checks manually with:

```bash
pre-commit run --all-files
```

Run `./prompts.sh --category <cat>` to generate prompts. The script
automatically refreshes `dataset/templates.json` from `rawdata.txt` before
launching the prompt interface.

Specify `--count N` and `--output FILE` for batch mode. Logs are written to
`${XDG_DATA_HOME:-$HOME/.local/share}/redteam/logs/prompts_sh.log`.









