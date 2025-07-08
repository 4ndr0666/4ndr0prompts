#!/usr/bin/env bash
set -euo pipefail

if ! command -v wl-copy >/dev/null 2>&1; then
    printf '\033[31m[ERROR]\033[0m wl-copy not found. Install with `sudo pacman -S wl-clipboard`.\n' >&2
    exit 1
fi

PYTHONPATH="$(cd "$(dirname "$0")/.." && pwd)"

mapfile -t slot_lines < <(python3 - <<'PY'
from promptlib import SLOTS
for k, vals in SLOTS.items():
    print(f"{k}:{'|'.join(vals)}")
PY
)

declare -A selections
for line in "${slot_lines[@]}"; do
    slot=${line%%:*}
    IFS='|' read -r -a opts <<< "${line#*:}"
    choice=$(printf '%s\n' "${opts[@]}" | fzf --prompt="${slot}> " --height=40% --border) || exit 130
    selections[$slot]=$choice
done

json="{"
first=1
for k in "${!selections[@]}"; do
    v=${selections[$k]}
    if [ $first -eq 0 ]; then json+=" ,"; fi
    json+="\"$k\":\"$v\""; first=0
done
json+="}"

prompt=$(SEL="$json" python3 - <<'PY'
import os, json
from collections import OrderedDict
from promptlib import assemble_prompt
sel=json.loads(os.environ['SEL'])
print(assemble_prompt(OrderedDict((k, sel[k]) for k in sel)))
PY
)

printf '%s\n' "$prompt"
printf '%s' "$prompt" | wl-copy
printf 'Copied to clipboard\n'
