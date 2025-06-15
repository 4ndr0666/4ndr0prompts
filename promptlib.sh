#!/bin/bash
# promptlib.sh - Production-ready shell wrapper for promptlib.py
set -euo pipefail

# -----------
# CONFIGURATION
# -----------

PYTHON_BIN="python3"
SCRIPT_NAME="promptlib.py"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/redteam-prompts"
LOG_FILE="$DATA_HOME/promptlib.log"
mkdir -p "$DATA_HOME"

# -----------
# USAGE FUNCTION
# -----------

usage() {
    printf 'Usage: %s --category <category> [--count N] [--output FILE] [--no-color]\n' "$0"
    printf '       %s --tui [--no-color]\n' "$0"
    printf '\n'
    printf '  --category <category>    Category key (batch mode, e.g. clothing_chest_exposure)\n'
    printf '  --count N                Number of prompts to generate (default: 5)\n'
    printf '  --output FILE            Output file saved under %s\n' "$DATA_HOME"
    printf '  --no-color               Disable cyan output highlighting\n'
    printf '  --tui                    Run interactive TUI mode\n'
    printf '\n'
    printf 'Available categories:\n'
    $PYTHON_BIN - <<'EOF'
from prompt_config import load_config
for name in sorted(load_config()[0].keys()):
    print(name)
EOF
}

# -----------
# ARGUMENT PARSING
# -----------

TUI_MODE=0
CATEGORY=""
COUNT=5
OUTPUT=""
NO_COLOR=0

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --tui)
            TUI_MODE=1
            shift
            ;;
        --category)
            CATEGORY="$2"
            shift; shift
            ;;
        --count)
            COUNT="$2"
            shift; shift
            ;;
        --output)
            OUTPUT="$DATA_HOME/$(basename "$2")"
            shift; shift
            ;;
        --no-color)
            NO_COLOR=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            printf '[ERROR] Unknown argument: %s\n' "$1"
            usage
            exit 1
            ;;
    esac
done

# -----------
# MAIN LOGIC
# -----------

if [[ "$TUI_MODE" -eq 1 ]]; then
    CMD=("$PYTHON_BIN" "$SCRIPT_NAME" "--tui")
    if [[ "$NO_COLOR" -eq 1 ]]; then
        CMD+=("--no-color")
    fi
    "${CMD[@]}"
    exit $?
fi

if [[ -z "$CATEGORY" ]]; then
    printf '[ERROR] --category is required unless running --tui\n'
    usage
    exit 1
fi

CMD=("$PYTHON_BIN" "$SCRIPT_NAME" "--category" "$CATEGORY" "--count" "$COUNT")
if [[ -n "$OUTPUT" ]]; then
    CMD+=("--output" "$OUTPUT")
fi
if [[ "$NO_COLOR" -eq 1 ]]; then
    CMD+=("--no-color")
fi

"${CMD[@]}"
STATUS=$?
if [[ $STATUS -eq 0 ]]; then
    printf '[SUCCESS] Prompts generated for category %s.\n' "$CATEGORY"
    printf '%s [SUCCESS] category=%s\n' "$(date -Is)" "$CATEGORY" >>"$LOG_FILE"
    if [[ -n "$OUTPUT" ]]; then
        printf '[INFO] See file: %s\n' "$OUTPUT"
        printf '%s [INFO] output=%s\n' "$(date -Is)" "$OUTPUT" >>"$LOG_FILE"
    fi
else
    printf '[ERROR] Prompt generation failed (exit code %s)\n' "$STATUS"
    printf '%s [ERROR] exit=%s\n' "$(date -Is)" "$STATUS" >>"$LOG_FILE"
fi



