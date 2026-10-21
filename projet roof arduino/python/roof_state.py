import json
import time
import os

DATA_DIR = os.path.join(
    os.path.dirname(__file__),
    "data"
)

os.makedirs(DATA_DIR, exist_ok=True)

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

    except:

        return {
            "state": "UNKNOWN",
            "position": -1,
            "timestamp": time.time()
        }