import os
import hashlib
import importlib
import promptlib as pl


def test_redteam_sha256():
    path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'redteam_dataset.txt')
    with open(path, 'rb') as f:
        data = f.read()
    assert hashlib.sha256(data).hexdigest() == 'd0312d7bc46e86ecacbeaadd76a76036206a7d9a845ea413464b87b4b3ce60fb'


def test_redteam_slots_populated():
    importlib.reload(pl)
    assert len(pl.SLOT_MAP['orientation']) >= 10
    assert len(pl.SLOT_MAP['pose']) >= len(pl.POSE_TAGS)
    assert len(pl.SLOT_MAP['action_sequence']) >= len(pl.ACTION_SEQUENCE_OPTIONS)
