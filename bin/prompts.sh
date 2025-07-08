#!/usr/bin/env bash
set -euo pipefail

command -v wl-copy >/dev/null 2>&1 || {
	echo "wl-copy not found" >&2
	exit 1
}
command -v fzf >/dev/null 2>&1 || {
	echo "fzf not found" >&2
	exit 1
}

# Get slot definitions from promptlib as JSON
slots_json=$(
	python3 - <<'PY'
import json, promptlib
print(json.dumps(promptlib.SLOTS))
PY
)

# Parse JSON using python to maintain minimal dependencies
slot_names=$(
	python3 - "$slots_json" <<'PY'
import json, sys
slots=json.loads(sys.argv[1])
for k in slots:
    print(k)
PY
)

prompt_parts=()
for slot in $slot_names; do
	options=$(
		python3 - "$slots_json" "$slot" <<'PY'
import json, sys
slots=json.loads(sys.argv[1])
slot=sys.argv[2]
print("\n".join(slots[slot]))
PY
	)
	selection=$(printf '%s\n' "$options" | fzf --prompt="${slot}: ")
	prompt_parts+=("$selection")
done

prompt=$(printf '%s ' "${prompt_parts[@]}" | sed 's/ $//')
printf '%s' "$prompt" | wl-copy
printf 'Prompt copied: %s\n' "$prompt"
