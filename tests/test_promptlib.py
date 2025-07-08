import promptlib
from collections import OrderedDict


def test_assemble_prompt():
    choices = OrderedDict([
        ("SUBJECT", "cat"),
        ("ACTION", "runs"),
        ("ADVERB", "quickly"),
    ])
    assert promptlib.assemble_prompt(choices) == "cat runs quickly"
