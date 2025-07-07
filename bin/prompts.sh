#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
IFS=$'\n\t'

choice=$(bin/choose_prompt.sh)

prompt=$(
	python3 - "$choice" <<'PY'
import sys
from canonical_loader import load_canonical
from prompt_config import generate_prompt

templates, slots, _ = load_canonical()
key = sys.argv[1]
template = templates.get(key)
slotset = slots.get(key, {})
if template is None:
    raise SystemExit(f"Unknown category: {key}")
print(generate_prompt(template, slotset))
PY
)

if command -v xclip >/dev/null 2>&1; then
	printf '%s' "$prompt" | xclip -selection clipboard
	echo "Copied to clipboard"
else
	printf '%s\n' "$prompt"
fi
