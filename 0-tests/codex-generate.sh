#!/usr/bin/env bash
set -euo pipefail
printf '🔄  Canonicalising raw dataset…\n'
python3 scripts/parse_rawdata.py --write
ruff check --fix .
black .
PYTHONPATH=. pytest -q



