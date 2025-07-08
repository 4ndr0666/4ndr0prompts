from __future__ import annotations
from collections import OrderedDict

# Canonical slot definitions
SLOTS = OrderedDict(
    {
        "subject": ["cat", "dog"],
        "style": ["photorealistic", "sketch"],
        "lighting": ["day", "night"],
    }
)

# Validate unique slot names
if len(SLOTS) != len(set(SLOTS.keys())):
    raise ValueError("Duplicate slot names in SLOTS")


def assemble(selections: dict[str, str]) -> str:
    """Assemble prompt from selections respecting slot order."""
    missing = set(SLOTS) - selections.keys()
    extra = selections.keys() - set(SLOTS)
    if missing or extra:
        raise ValueError(f"Invalid slots: missing {missing} extra {extra}")
    return " ".join(selections[slot] for slot in SLOTS)


if __name__ == "__main__":
    import json

    print(json.dumps(SLOTS))
