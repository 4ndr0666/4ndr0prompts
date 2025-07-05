import json
import canonical_loader as cl


def test_list_categories(tmp_path):
    data = {"templates": {"pose": "t"}, "slots": {"pose": {"tag": ["a"]}}}
    cfg = tmp_path / "templates.json"
    cfg.write_text(json.dumps(data), encoding="utf-8")
    plugdir = tmp_path / "plugins"
    plugdir.mkdir()
    cats = cl.list_categories(str(cfg), str(plugdir))
    assert cats == ["pose"]


def test_list_slots(tmp_path):
    data = {"templates": {"pose": "t"}, "slots": {"pose": {"tag": ["a"]}}}
    cfg = tmp_path / "templates.json"
    cfg.write_text(json.dumps(data), encoding="utf-8")
    plugdir = tmp_path / "plugins"
    plugdir.mkdir()
    slots = cl.list_slots("pose", str(cfg), str(plugdir))
    assert slots == {"tag": ["a"]}
