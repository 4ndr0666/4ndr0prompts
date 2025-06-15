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


