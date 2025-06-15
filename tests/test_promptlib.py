import promptlib


def test_generate_prompt_wrapper():
    template = "Hello [NAME]"
    slots = {"NAME": ["Alice", "Bob"]}
    result = promptlib.generate_prompt(template, slots)
    assert result in {"Hello Alice", "Hello Bob"}


def test_random_prompt_selection():
    template = "Hi [WHO]"
    slots = {"WHO": ["A", "B"]}
    prompt, selected = promptlib.random_prompt(template, slots)
    assert prompt in {"Hi A", "Hi B"}
    assert selected
    assert selected["WHO"] in {"A", "B"}
