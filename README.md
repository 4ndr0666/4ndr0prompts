# 4ndr0prompts

This repository contains utilities for generating and testing red-team prompt mutations. Development follows strict linting and testing rules.

## Setup

1. Install the development dependencies:
   ```bash
   pip install -r requirements.txt  # if available
   pip install pre-commit
   ```
2. Install the pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

- All code changes must pass **ruff**, **black**, **pytest**, and the merge-artifact scrubber `0-tests/codex-merge-clean.sh`.
- The hooks run automatically via pre-commit and should also run in CI for every pull request that modifies code files.
- Documentation-only updates can skip these checks, but mixed changes run the full suite.

Run all checks manually with:

```bash
pre-commit run --all-files
```

## CLI and TUI

The toolkit ships with several interfaces:

* **promptlib_cli.py** – interactive CLI using `prompt_toolkit`.
  Install the dependency and run:

  ```bash
  pip install prompt_toolkit
  python promptlib_cli.py
  ```

* **promptlib_tui.py** – fullscreen TUI based on `npyscreen`.
  It requires a real terminal:

  ```bash
  pip install npyscreen
  python promptlib_tui.py
  ```

* **promptlib_interactive.py** – fallback CLI/TUI wrapper.
  Run with no arguments for the interactive menu or pass flags for CLI mode.

* **promptlib.sh** – shell helper for scripted usage. View options with:

  ```bash
  ./promptlib.sh --help
  ```

## Running Tests

Scrub merge artifacts before linting or testing:

```bash
0-tests/codex-merge-clean.sh <file ...>
```

Then execute the linters and unit tests:

```bash
ruff .
black .
PYTHONPATH=. pytest -q
```

Refer to `AGENTS.md` for full workflow and policy guidelines.

