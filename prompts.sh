#!/bin/sh
# promptlib.sh - Production-ready shell wrapper for promptlib.py and pipeline
set -eu

# -----------
# CONFIGURATION
# -----------

PYTHON_BIN="python3"
TUI_SCRIPT="tests/ui/promptlib_tui.py"
CLI_SCRIPT="promptlib.py"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/prompts.sh"
LOG_FILE="$DATA_HOME/prompts_sh.log"
mkdir -p "$DATA_HOME"

# -----------
# USAGE FUNCTION
# -----------

usage() {
    printf 'Usage: %s [--cli --category <category> [--count N] [--output FILE]] [--pipeline] [--no-color] [--dry-run]\n' "$0"
    printf '\n'
    printf '  --cli                    Run minimal CLI instead of default TUI\n'
    printf '  --category <category>    Category key for CLI mode\n'
    printf '  --count N                Number of prompts to generate (default: 5)\n'
    printf '  --output FILE            Output file saved under %s\n' "$DATA_HOME"
    printf '  --no-color               Disable cyan output highlighting\n'
    printf '  --dry-run                Print command without executing\n'
    printf '  --pipeline               Run full automation pipeline\n'
    printf '\n'
    printf 'Available categories:\n'
    "$PYTHON_BIN" "$TUI_SCRIPT" --simple-cli --list-categories
}

# -----------
# ARGUMENT PARSING
# -----------

CLI_MODE=0
CATEGORY=""
COUNT=5
OUTPUT=""
NO_COLOR=0
DRY_RUN=0
PIPELINE=0

while [ "$#" -gt 0 ]; do
    key="$1"
    case "$key" in
        --cli)
            CLI_MODE=1
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
        --pipeline)
            PIPELINE=1
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
# PIPELINE FUNCTION
# -----------

run_pipeline() {
    REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
    CMD="${PYTHON_BIN} ${REPO_DIR}/scripts/parse_rawdata.py --force"
    if [ "$DRY_RUN" -eq 1 ]; then
        printf '[DRY-RUN] %s\n' "$CMD"
    else
        eval "$CMD"
    fi
    FILES=$(git ls-files '*.py' '*.sh')
    chmod 755 0-tests/codex-generate.sh
    bash 0-tests/codex-generate.sh "$FILES"
    ruff check --fix .
    black .
    PYTHONPATH=. pytest -q
}

# -----------
# MAIN LOGIC
# -----------

if [ "$PIPELINE" -eq 1 ]; then
    run_pipeline
    exit $?
fi

if [ "$CLI_MODE" -eq 0 ]; then
    set -- "$PYTHON_BIN" "$TUI_SCRIPT"
    if [ "$NO_COLOR" -eq 1 ]; then
        set -- "$@" --no-color
    fi
    if [ "$DRY_RUN" -eq 1 ]; then
        printf '[DRY-RUN] %s\n' "$*"
        exit 0
    fi
    PYTHONPATH=. "$@"
    exit $?
fi

if [ -z "$CATEGORY" ]; then
    printf '[ERROR] --category is required with --cli\n'
    usage
    exit 1
fi
set -- "$PYTHON_BIN" "$CLI_SCRIPT" --category "$CATEGORY" --count "$COUNT"
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

PYTHONPATH=. "$@"
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
