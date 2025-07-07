#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
IFS=$'\n\t'

templates_file="${1:-data/templates.yaml}"

if ! [ -f "$templates_file" ]; then
	echo "Templates file not found: $templates_file" >&2
	exit 1
fi

choice=$(grep -o '^[^:]*' "$templates_file" | fzf --prompt='Template > ' --height=40% --border) || exit 1
printf '%s\n' "$choice"
