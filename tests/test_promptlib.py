import promptlib


def test_assemble_valid():
    selections = {"subject": "cat", "style": "photorealistic", "lighting": "day"}
    assert promptlib.assemble(selections) == "cat photorealistic day"


def test_invalid_slot():
    selections = {"subject": "cat", "style": "photorealistic"}
    try:
        promptlib.assemble(selections)
    except ValueError as e:
        assert "missing" in str(e)
    else:
        assert False, "Expected ValueError"
