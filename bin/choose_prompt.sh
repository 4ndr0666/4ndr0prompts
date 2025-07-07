#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
IFS=$'\n\t'

choice=$(
	python3 - <<'PY'
from canonical_loader import list_categories
for c in list_categories():
    print(c)
PY
)

choice=$(printf '%s\n' "$choice" | fzf --prompt='Category > ' --height=40% --border) || exit 1
printf '%s\n' "$choice"
