import promptlib as pl


def test_slots_defined():
    assert pl.SLOTS
    pl.validate_slots()


def test_slot_order():
    assert pl.SLOTS == list(pl.SLOT_MAP.keys())
