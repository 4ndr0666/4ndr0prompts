#!/usr/bin/env python3
"""Parse AGENTS.md and emit ticket markdown files."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AGENTS = ROOT / "AGENTS.md"
TICKETS_DIR = ROOT / "tickets"

pattern = re.compile(
    r"\|\s*\*\*(\d+-\d+)\*\*\s*\|\s*(\w+)\s*\|\s*(.*?)\s*\|\s*([\w,-]*)\s*\|\s*(P\d)\s*\|\s*(\d+)\s*\|"
)

lines = AGENTS.read_text(encoding="utf-8").splitlines()
for line in lines:
    m = pattern.search(line)
    if not m:
        continue
    ticket_id, stream, title, deps, priority, hours = m.groups()
    content = (
        f"# {ticket_id} - {stream} - {title}\n"
        f"- **Stream**: {stream}\n"
        f"- **Title**: {title}\n"
        f"- **Dependencies**: {deps or 'None'}\n"
        f"- **Priority**: {priority}\n"
        f"- **Estimated hours**: {hours}\n"
    )
    outfile = TICKETS_DIR / f"{ticket_id}.md"
    outfile.write_text(content, encoding="utf-8")
