import threading
import time
import uvicorn

from dome_server import app as dome_app
from server_safety import app as safety_app

def run_dome():
    uvicorn.run(
        dome_app,
        host="0.0.0.0",
        port=11111,
        log_level="info"
    )


def run_safety():
    uvicorn.run(
        safety_app,
        host="0.0.0.0",
        port=11112,
        log_level="info"
    )


if __name__ == "__main__":

    print("==================================")
    print(" Observatory Server")
    print("==================================")
    print("Starting Dome Server :11111")
    print("Starting Safety Server :11112")

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