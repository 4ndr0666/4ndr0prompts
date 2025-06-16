#!/bin/sh
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
    printf 'Usage: %s --category <category> [--count N] [--output FILE] [--no-color] [--dry-run]\n' "$0"
    printf '       %s --tui [--no-color] [--dry-run]\n' "$0"
    printf '\n'
    printf '  --category <category>    Category key (batch mode, e.g. clothing_chest_exposure)\n'
    printf '  --count N                Number of prompts to generate (default: 5)\n'
    printf '  --output FILE            Output file saved under %s\n' "$DATA_HOME"
    printf '  --no-color               Disable cyan output highlighting\n'
    printf '  --dry-run                Print command without executing\n'
    printf '  --tui                    Run interactive TUI mode\n'
    printf '\n'
    printf 'Available categories:\n'
    "$PYTHON_BIN" "$SCRIPT_NAME" --list-categories
}

# -----------
# ARGUMENT PARSING
# -----------

TUI_MODE=0
CATEGORY=""
COUNT=5
OUTPUT=""
NO_COLOR=0
DRY_RUN=0

while [ "$#" -gt 0 ]; do
    key="$1"
    case "$key" in
        --tui)
            TUI_MODE=1
            shift
            ;;
        --category)
            CATEGORY="$2"
            shift 2
            ;;
        --count)
            COUNT="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$DATA_HOME/$(basename "$2")"
            shift 2
            ;;
        --no-color)
            NO_COLOR=1
            shift
            ;;
        --dry-run)
            DRY_RUN=1
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

if [ "$TUI_MODE" -eq 1 ]; then
    set -- "$PYTHON_BIN" "$SCRIPT_NAME" --tui
    if [ "$NO_COLOR" -eq 1 ]; then
        set -- "$@" --no-color
    fi
    if [ "$DRY_RUN" -eq 1 ]; then
        printf '[DRY-RUN] %s\n' "$*"
        exit 0
    fi
    "$@"
    exit $?
fi

if [ -z "$CATEGORY" ]; then
    printf '[ERROR] --category is required unless running --tui\n'
    usage
    exit 1
fi

set -- "$PYTHON_BIN" "$SCRIPT_NAME" --category "$CATEGORY" --count "$COUNT"
if [ -n "$OUTPUT" ]; then
    set -- "$@" --output "$OUTPUT"
fi
if [ "$NO_COLOR" -eq 1 ]; then
    set -- "$@" --no-color
fi

if [ "$DRY_RUN" -eq 1 ]; then
    printf '[DRY-RUN] %s\n' "$*"
    exit 0
fi

"$@"
STATUS=$?
if [ "$STATUS" -eq 0 ]; then
    printf '[SUCCESS] Prompts generated for category %s.\n' "$CATEGORY"
    if [ "$DRY_RUN" -eq 0 ]; then
        printf '%s [SUCCESS] category=%s\n' "$(date -Is)" "$CATEGORY" >>"$LOG_FILE"
    fi
    if [ -n "$OUTPUT" ]; then
        printf '[INFO] See file: %s\n' "$OUTPUT"
        if [ "$DRY_RUN" -eq 0 ]; then
            printf '%s [INFO] output=%s\n' "$(date -Is)" "$OUTPUT" >>"$LOG_FILE"
        fi
    fi
else
    printf '[ERROR] Prompt generation failed (exit code %s)\n' "$STATUS"
    if [ "$DRY_RUN" -eq 0 ]; then
        printf '%s [ERROR] exit=%s\n' "$(date -Is)" "$STATUS" >>"$LOG_FILE"
    fi
fi




