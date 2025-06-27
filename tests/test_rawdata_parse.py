from scripts import parse_rawdata


def test_all_categories_accounted():
    lines = parse_rawdata._read_raw(parse_rawdata.RAWDATA_PATH)
    templates, slots = parse_rawdata.parse_lines(lines, trim_sentences=1)
    for cat in list(parse_rawdata.CATEGORY_RULES.keys()) + [
        parse_rawdata.DEFAULT_CATEGORY
    ]:
        assert cat in templates
        assert cat in slots


def test_no_empty_slot_lists(tmp_path):
    out_dir = tmp_path
    parse_rawdata.write_outputs({"a": "b"}, {"a": {"S": ["x"]}}, out_dir)
    report = out_dir / "slots_report.tsv"
    assert report.exists()
    lines = report.read_text().splitlines()
    for line in lines:
        assert len(line.split("\t")) == 3


def test_no_duplicate_slot_values():
    lines = parse_rawdata._read_raw(parse_rawdata.RAWDATA_PATH)
    _, slots = parse_rawdata.parse_lines(lines)
    for cat, slot_map in slots.items():
        for values in slot_map.values():
            assert len(values) == len(set(values))


def test_needs_update(tmp_path):
    raw = tmp_path / "raw.txt"
    raw.write_text("x")
    assert parse_rawdata.needs_update(str(raw), str(tmp_path))
    parse_rawdata.write_outputs({"a": "b"}, {"a": {}}, str(tmp_path))
    assert not parse_rawdata.needs_update(str(raw), str(tmp_path))
    import time

    time.sleep(1)
    raw.write_text("y")
    assert parse_rawdata.needs_update(str(raw), str(tmp_path))
