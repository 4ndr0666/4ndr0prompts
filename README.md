# 4ndr0prompts

Tools for generating and manipulating red-team prompts.

## Configuration

Prompt templates and slot lists live in `dataset/templates.json`. The `prompt_config.py` module loads and caches this file and exposes `load_config()` for use by the CLI, TUI and shell wrappers.

## Development Workflow

1. Remove merge artifacts:
   ```bash
   0-tests/codex-merge-clean.sh $(git ls-files '*.sh' '*.py')
   ```
2. Apply formatting:
   ```bash
   ruff --fix . && black .
   ```
3. Run tests:
   ```bash
   PYTHONPATH=. pytest -q
   ```
4. Commit and run pre-commit hooks:
   ```bash
   git add -u && git commit -m "<type>: <message>"
   pre-commit run --all-files
   ```
