#!/usr/bin/env bash
set -euo pipefail

command -v wl-copy >/dev/null 2>&1 || {
	echo "wl-copy required" >&2
	exit 1
}
command -v fzf >/dev/null 2>&1 || {
	echo "fzf required" >&2
	exit 1
}

readarray -t SLOTS < <(
	python3 - <<'PY'
import promptlib as pl
for s in pl.SLOTS:
    print(s)
PY
)

build_line() {
	slot="$1"
	python3 - "$slot" <<'PY'
import sys, promptlib as pl
slot = sys.argv[1]
for o in pl.SLOT_MAP[slot]:
    print(o)
PY
}

prompt_lines=()
for slot in "${SLOTS[@]}"; do
	readarray -t opts < <(build_line "$slot")
	sel=$(printf '%s\n' "${opts[@]}" | fzf --prompt="$slot: ")
	prompt_lines+=("${slot^}: $sel")
done

printf '> {\n%s\n}' "$(printf '    %s\n' "${prompt_lines[@]}")" | wl-copy
printf 'Prompt copied to clipboard.\n'
