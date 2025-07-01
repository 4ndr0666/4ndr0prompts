#!/usr/bin/env bash
set -euo pipefail
printf '🔄  Canonicalising raw dataset…\n'
python3 scripts/parse_rawdata.py --force
printf '\n🔎  Linting and type checking…\n'
ruff check --fix .
black .
shellcheck -x prompts.sh
mypy promptlib.py prompt_config.py
bandit -r .
PYTHONPATH=. pytest -q




