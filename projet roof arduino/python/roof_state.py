import json
import time

STATE_FILE = "roof_state.json"


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