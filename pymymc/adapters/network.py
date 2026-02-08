from __future__ import annotations

import requests

_TEST_URL = "https://1.1.1.1/"


def check_internet() -> bool:
    try:
        resp = requests.get(_TEST_URL, timeout=4)
        return resp.status_code == 200
    except requests.ConnectionError:
        return False
