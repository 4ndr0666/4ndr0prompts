import json
import threading
import time
import urllib.request

import server


def start_server(port: int = 8765):
    th = threading.Thread(target=server.run, kwargs={"port": port}, daemon=True)
    th.start()
    time.sleep(0.2)
    return port


def test_categories_endpoint():
    port = start_server()
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/categories") as resp:
        data = json.load(resp)
    assert "clothing_chest_exposure" in data


def test_slots_endpoint():
    port = start_server()
    url = f"http://127.0.0.1:{port}/slots/clothing_chest_exposure"
    with urllib.request.urlopen(url) as resp:
        data = json.load(resp)
    assert "PERSON" in data
