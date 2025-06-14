import subprocess
import sys

import promptlib2


def test_load_prompts_nonempty():
    prompts = promptlib2.load_prompts()
    assert prompts, "dataset should not be empty"
    unique_prompts = {p.prompt for p in prompts}
    assert len(unique_prompts) == len(prompts)


def test_random_prompt_has_category():
    entry = promptlib2.get_random_prompts(1)[0]
    assert entry.category
    assert entry.prompt


def test_cli_dry_run():
    result = subprocess.run(
        [sys.executable, "promptlib2.py", "--dry-run", "--count", "1"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip()
