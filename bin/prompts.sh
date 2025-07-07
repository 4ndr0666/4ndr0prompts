#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
IFS=$'\n\t'

choice=$(bin/choose_prompt.sh)
template_key="$choice"

prompt=$(
	python3 - "$template_key" <<'PY'
import sys
import yaml
from lib.promptgen import generate_prompt

with open('data/templates.yaml') as f:
    templates = yaml.safe_load(f)
with open('data/slots.yaml') as f:
    slots = yaml.safe_load(f)

key = sys.argv[1]
print(generate_prompt(templates[key], slots))
PY
)

if command -v xclip >/dev/null 2>&1; then
	printf '%s' "$prompt" | xclip -selection clipboard
	echo "Copied to clipboard"
else
	printf '%s\n' "$prompt"
fi
