# 4ndr0prompts

This repository contains utilities for generating red-team prompt mutations. The interface is driven entirely by `promptlib_cli.py` which uses `prompt_toolkit` for fuzzy, colorised menus. Use the `prompts.sh` script as the single entrypoint.

## Setup

1. Install development dependencies:
   ```bash
   pip install pre-commit ruff black pytest shellcheck
   ```
2. Install the pre-commit hooks:
   ```bash
   pre-commit install
   ```
3. Hooks run `0-tests/codex-merge-clean.sh` and then execute **ruff**, **black**, **shellcheck**, and **pytest** on changed files.

## Usage

Run the CLI via:

```bash
./prompts.sh
```

All categories and slots are loaded dynamically from `dataset/templates.json`. The category selector previews available slots, and previews can be regenerated until you save. Updating the dataset automatically updates the menu options without code changes.

## Development Workflow

- All code changes must pass **ruff**, **black**, **pytest**, and the merge-artifact scrubber `0-tests/codex-merge-clean.sh`.
- Documentation-only updates can skip these checks, but mixed changes run the full suite.

Run all checks manually with:

```bash
pre-commit run --all-files
```

To regenerate the template dataset in verbatim mode:

```bash
PYTHONPATH=. python scripts/parse_rawdata.py --write --trim-sentences 1
```
