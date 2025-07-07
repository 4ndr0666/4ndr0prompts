from lib.promptgen import generate_prompt


def test_generate_prompt():
    template = "hello {name}"
    slots = {"name": "world"}
    assert generate_prompt(template, slots) == "hello world"
