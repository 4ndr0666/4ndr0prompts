#!/usr/bin/env python3
"""Minimal prompt library.
Defines slot order and options used by prompts.sh."""
from collections import OrderedDict

SLOTS = OrderedDict([
    ("SUBJECT", ["cat", "dog", "robot"]),
    ("ACTION", ["runs", "jumps", "sleeps"]),
    ("ADVERB", ["quickly", "slowly", "gracefully"]),
])

TEMPLATE = "{SUBJECT} {ACTION} {ADVERB}"


def assemble_prompt(choices: OrderedDict) -> str:
    """Assemble the final prompt using TEMPLATE."""
    return TEMPLATE.format(**choices)


if __name__ == "__main__":
    import json
    print(json.dumps(SLOTS))
