#!/usr/bin/env bash
# prompts.sh - Wrapper for promptlib_cli.py (auto-installs prompt_toolkit)
set -euo pipefail

PYTHON_BIN="python3"
SCRIPT="promptlib_cli.py"

# Auto-install prompt_toolkit if missing
if ! "$PYTHON_BIN" - >/dev/null 2>&1 <<'PYEOF'
import importlib.util, sys
sys.exit(0 if importlib.util.find_spec('prompt_toolkit') else 1)
PYEOF
then
    printf '[INFO] Installing prompt_toolkit…\n'
    "$PYTHON_BIN" -m pip install --quiet --user prompt_toolkit || {
        printf '[ERROR] Failed to install prompt_toolkit\n'
        exit 1
    }
fi

exec "$PYTHON_BIN" "$SCRIPT" "$@"
