import json
from pathlib import Path

import yaml
import plugin_loader as pl


def _write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data), encoding="utf-8")


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def _write_markdown(path: Path, yaml_block: dict, json_block: dict) -> None:
    md = """```yaml
{yaml}
```
```json
{json}
```""".format(
        yaml=yaml.safe_dump(yaml_block), json=json.dumps(json_block)
    )
    path.write_text(md, encoding="utf-8")


def test_load_plugins_dedup_and_uncategorized(tmp_path: Path) -> None:
    yaml_file = tmp_path / "p1.yaml"
    _write_yaml(yaml_file, {"pose": ["stand", "sit", "stand"]})
    json_file = tmp_path / "p2.json"
    _write_json(json_file, {"pose": ["jump"], "unknown": ["x"]})

    result = pl.load_plugin_dir(tmp_path)
    assert result["pose"] == ["jump", "sit", "stand"]
    assert "uncategorized" in result and result["uncategorized"] == ["x"]


def test_markdown_and_normalisation(tmp_path: Path) -> None:
    md_file = tmp_path / "p.md"
    _write_markdown(
        md_file,
        {"Camera Move": ["zoom"]},
        {"lighting": ["soft"], "camera-move": ["pan"]},
    )
    result = pl.load_plugin_dir(tmp_path)
    assert result["camera_move"] == ["pan", "zoom"]
    assert result["lighting"] == ["soft"]
