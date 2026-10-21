import threading
import time
import uvicorn

from config import (
    DOME_PORT,
    SAFETY_PORT,
    VERSION
)

from dome_server import app as dome_app
from server_safety import app as safety_app


def run_dome():

    uvicorn.run(
        dome_app,
        host="0.0.0.0",
        port=DOME_PORT,
        log_level="info"
    )


def run_safety():

    uvicorn.run(
        safety_app,
        host="0.0.0.0",
        port=SAFETY_PORT,
        log_level="info"
    )


if __name__ == "__main__":

    print("==================================")
    print(f" Observatory Server {VERSION}")
    print("==================================")
    print(f"Starting Dome Server   : {DOME_PORT}")
    print(f"Starting Safety Server : {SAFETY_PORT}")

    threading.Thread(
        target=run_dome,
        daemon=True
    ).start()

    threading.Thread(
        target=run_safety,
        daemon=True
    ).start()

    while True:
        time.sleep(1)