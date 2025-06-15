import subprocess
import sys
import os

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


def test_default_log_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    import importlib

    promptlib = importlib.import_module("promptlib")
    importlib.reload(promptlib)
    expected = os.path.join(tmp_path, "redteam-prompts", "logs")
    assert promptlib.DEFAULT_LOG_DIR == expected
