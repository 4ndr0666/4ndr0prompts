import json
import time
from pathlib import Path

import canonical_loader as cl


def test_hot_reload(tmp_path: Path) -> None:
    cfg = tmp_path / "templates.json"
    cfg.write_text(
        json.dumps({"templates": {}, "slots": {"pose": ["a"]}}), encoding="utf-8"
    )
    plugdir = tmp_path / "plugins"
    plugdir.mkdir()
    (plugdir / "p.json").write_text(json.dumps({"pose": ["jump"]}), encoding="utf-8")

    _, _, plugins = cl.load_canonical(str(cfg), str(plugdir))
    assert plugins["pose"] == ["jump"]

    time.sleep(0.01)
    (plugdir / "p2.json").write_text(json.dumps({"pose": ["sit"]}), encoding="utf-8")
    _, _, plugins2 = cl.load_canonical(str(cfg), str(plugdir))
    assert "sit" in plugins2["pose"]
