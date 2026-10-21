import json
import time
import os
import sys


def get_base_path():

    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.dirname(__file__)


BASE_DIR = get_base_path()

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

STATE_FILE = os.path.join(
    DATA_DIR,
    "roof_state.json"
)


def save_state(data):

    with open(
        STATE_FILE,
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )


def load_state():

    try:

        with open(
            STATE_FILE,
            "r",
            encoding="utf8"
        ) as f:

            return json.load(f)

    except Exception:

        return {
            "state": "UNKNOWN",
            "position": -1,
            "timestamp": time.time()
        }
