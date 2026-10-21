from fastapi import FastAPI
import time

from config import *
from roof_serial import RoofController
from roof_state import (
    load_state,
    save_state
)

from dome_model import (
    state_to_shutter_status,
    is_slewing
)

from roof_monitor import RoofMonitor
from logger import log

from mount_control import (
    ensure_mount_parked
)

app = FastAPI()

roof = RoofController(
    SERIAL_PORT,
    BAUDRATE
)

server_transaction = 0

state_data = load_state()

connected = False

last_motion = "CLOSING"


def alpaca_response(value=None):

    global server_transaction

    server_transaction += 1

    result = {
        "ClientTransactionID": 0,
        "ServerTransactionID": server_transaction,
        "ErrorNumber": 0,
        "ErrorMessage": ""
    }

    if value is not None:
        result["Value"] = value

    return result


def compute_position():

    state = state_data["state"]

    if state == "OPENED":
        return 100

    if state == "CLOSED":
        return 0

    if state not in [
        "OPENING",
        "CLOSING"
    ]:
        return state_data["position"]

    elapsed = (
        time.time()
        - state_data["timestamp"]
    )

    delta = (
        elapsed /
        FULL_TRAVEL_TIME
    ) * 100

    start = state_data["position"]

    if state == "OPENING":

        return min(
            100,
            int(start + delta)
        )

    return max(
        0,
        int(start - delta)
    )


def sync_state():

    try:

        arduino_state = roof.status()

        if arduino_state == "OPENED":

            state_data["state"] = "OPENED"
            state_data["position"] = 100

        elif arduino_state == "CLOSED":

            state_data["state"] = "CLOSED"
            state_data["position"] = 0

        elif arduino_state == "STOPPED":

            state_data["position"] = compute_position()

        elif arduino_state == "ERROR":

            state_data["position"] = compute_position()
            state_data["state"] = "ERROR"

        elif arduino_state == "UNKNOWN":

            state_data["state"] = "UNKNOWN"

        elif arduino_state == "OPENING":

            state_data["state"] = "OPENING"

        elif arduino_state == "CLOSING":

            state_data["state"] = "CLOSING"

        save_state(state_data)

        return arduino_state

    except Exception as ex:

        print(ex)

        return "ERROR"


monitor = RoofMonitor(sync_state)
monitor.start()


@app.get("/")
def root():

    return {
        "name": "Observatory Roof",
        "version": "1.0"
    }


@app.get("/management/apiversions")
def apiversions():

    return [1]


@app.get("/management/v1/configureddevices")
def configureddevices():

    return [
        {
            "DeviceName": "Observatory Roof",
            "DeviceType": "Dome",
            "DeviceNumber": 0,
            "UniqueID": "Roof001"
        }
    ]


@app.get("/status")
def status():

    sync_state()

    return {
        "state": state_data["state"],
        "position": compute_position()
    }


@app.get("/roof/info")
def roof_info():

    sync_state()

    return {
        "state": state_data["state"],
        "position": compute_position(),
        "slewing": is_slewing(
            state_data["state"]
        )
    }


@app.put("/api/v1/dome/0/openshutter")
def open_shutter():

    global last_motion

    if not ensure_mount_parked():

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": server_transaction,
            "ErrorNumber": 1024,
            "ErrorMessage": "Mount parking failed"
        }

    last_motion = "OPENING"

    sync_state()

    position = compute_position()

    if position < 0:
        position = 0

    roof.open()

    log("OPEN command")

    state_data["state"] = "OPENING"
    state_data["position"] = position
    state_data["timestamp"] = time.time()

    save_state(state_data)

    return alpaca_response()


@app.put("/api/v1/dome/0/closeshutter")
def close_shutter():

    global last_motion

    if not ensure_mount_parked():

        return {
            "ClientTransactionID": 0,
            "ServerTransactionID": server_transaction,
            "ErrorNumber": 1024,
            "ErrorMessage": "Mount parking failed"
        }

    last_motion = "CLOSING"

    sync_state()

    position = compute_position()

    if position < 0:
        position = 100

    roof.close()

    log("CLOSE command")

    state_data["state"] = "CLOSING"
    state_data["position"] = position
    state_data["timestamp"] = time.time()

    save_state(state_data)

    return alpaca_response()


@app.put("/api/v1/dome/0/abortslew")
def abortslew():

    global last_motion

    state_data["position"] = compute_position()

    roof.stop()

    log("STOP command")

    state_data["state"] = last_motion

    save_state(state_data)

    return alpaca_response()


@app.get("/api/v1/dome/0/shutterstatus")
def shutterstatus():

    state = state_data["state"]

    return alpaca_response(
        state_to_shutter_status(state)
    )


@app.get("/api/v1/dome/0/slewing")
def slewing():

    return alpaca_response(
        is_slewing(
            state_data["state"]
        )
    )


@app.get("/api/v1/dome/0/connected")
def get_connected():

    return alpaca_response(
        connected
    )


@app.put("/api/v1/dome/0/connected")
def set_connected():

    global connected

    connected = True

    print("NINA CONNECTED")

    return alpaca_response()


@app.get("/api/v1/dome/0/name")
def name():

    return alpaca_response(
        "Observatory Roof"
    )


@app.get("/api/v1/dome/0/description")
def description():

    return alpaca_response(
        "Arduino Nano + BTS7960 Roof Controller"
    )


@app.get("/api/v1/dome/0/driverinfo")
def driverinfo():

    return alpaca_response(
        "Python FastAPI Alpaca Roof"
    )


@app.get("/api/v1/dome/0/driverversion")
def driverversion():

    return alpaca_response(
        "1.0.0"
    )


@app.get("/api/v1/dome/0/interfaceversion")
def interfaceversion():

    return alpaca_response(1)


@app.get("/api/v1/dome/0/cansetshutter")
def cansetshutter():

    return alpaca_response(True)


@app.get("/api/v1/dome/0/canfindhome")
def canfindhome():

    return alpaca_response(False)


@app.get("/api/v1/dome/0/canpark")
def canpark():

    return alpaca_response(False)


@app.get("/api/v1/dome/0/cansetpark")
def cansetpark():

    return alpaca_response(False)


@app.get("/api/v1/dome/0/canslave")
def canslave():

    return alpaca_response(False)


@app.get("/api/v1/dome/0/slaved")
def slaved():

    return alpaca_response(False)


@app.get("/api/v1/dome/0/cansetazimuth")
def cansetazimuth():

    return alpaca_response(False)


@app.get("/api/v1/dome/0/cansyncazimuth")
def cansyncazimuth():

    return alpaca_response(False)


@app.get("/api/v1/dome/0/athome")
def athome():

    return alpaca_response(False)


@app.get("/api/v1/dome/0/atpark")
def atpark():

    return alpaca_response(False)


@app.get("/api/v1/dome/0/azimuth")
def azimuth():

    return alpaca_response(0.0)


@app.get("/api/v1/dome/0/altitude")
def altitude():

    return alpaca_response(0.0)


@app.get("/api/v1/dome/0/supportedactions")
def supportedactions():

    return alpaca_response([])
