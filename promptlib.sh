#!/bin/bash
# promptlib.sh - Production-ready shell wrapper for promptlib.py

# -----------
# CONFIGURATION
# -----------

PYTHON_BIN="python3"
SCRIPT_NAME="promptlib.py"

# -----------
# USAGE FUNCTION
# -----------

usage() {
    echo "Usage: $0 --category <category> [--count N] [--output FILE] [--no-color]"
    echo "       $0 --tui [--no-color]"
    echo
    echo "  --category <category>    Category key (batch mode, e.g. clothing_chest_exposure)"
    echo "  --count N                Number of prompts to generate (default: 5)"
    echo "  --output FILE            Output file for structured prompts"
    echo "  --no-color               Disable cyan output highlighting"
    echo "  --tui                    Run interactive TUI mode"
    echo
    echo "Available categories:"
    $PYTHON_BIN $SCRIPT_NAME --help | grep "choices=" | sed 's/.*choices=//' | tr -d '[],' | tr "'" "\n" | awk '{$1=$1};1' | grep -v "^$" | sort | uniq
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
            OUTPUT="$2"
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
            echo "[ERROR] Unknown argument: $1"
            usage
            exit 1
            ;;
    esac
done

# -----------
# MAIN LOGIC
# -----------

if [[ "$TUI_MODE" -eq 1 ]]; then
    CMD="$PYTHON_BIN $SCRIPT_NAME --tui"
    if [[ "$NO_COLOR" -eq 1 ]]; then
        CMD="$CMD --no-color"
    fi
    eval $CMD
    exit $?
fi

if [[ -z "$CATEGORY" ]]; then
    echo "[ERROR] --category is required unless running --tui"
    usage
    exit 1
fi

CMD="$PYTHON_BIN $SCRIPT_NAME --category $CATEGORY --count $COUNT"
if [[ ! -z "$OUTPUT" ]]; then
    CMD="$CMD --output \"$OUTPUT\""
fi
if [[ "$NO_COLOR" -eq 1 ]]; then
    CMD="$CMD --no-color"
fi

eval $CMD
STATUS=$?
if [[ $STATUS -eq 0 ]]; then
    echo "[SUCCESS] Prompts generated for category '$CATEGORY'."
    if [[ ! -z "$OUTPUT" ]]; then
        echo "[INFO] See file: $OUTPUT"
    fi
else
    echo "[ERROR] Prompt generation failed (exit code $STATUS)"
fi

