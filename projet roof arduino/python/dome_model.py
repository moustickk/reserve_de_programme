def state_to_shutter_status(state):

    mapping = {
        "OPENED": 0,
        "CLOSED": 1,
        "OPENING": 2,
        "CLOSING": 3,
        "ERROR": 4,
        "UNKNOWN": 4
    }

    return mapping.get(state, 4)


def is_slewing(state):

    return state in [
        "OPENING",
        "CLOSING"
    ]