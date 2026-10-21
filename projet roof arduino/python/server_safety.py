from fastapi import FastAPI
import threading
import uvicorn

import safety

app = FastAPI()

monitor_started = False


def ensure_monitor_started():
    global monitor_started

    if not monitor_started:
        threading.Thread(
            target=safety.weather_monitor_loop,
            daemon=True
        ).start()

        monitor_started = True


@app.on_event("startup")
def startup_event():
    ensure_monitor_started()


@app.get("/api/v1/safetymonitor/0/issafe")
def issafe():
    with safety.state_lock:
        return {
            "Value": safety.is_safe,
            "ErrorNumber": 0,
            "ErrorMessage": ""
        }


@app.get("/api/v1/safetymonitor/0/name")
def name():
    return {
        "Value": "Meteo Safety Monitor (Open-Meteo)",
        "ErrorNumber": 0,
        "ErrorMessage": ""
    }


@app.get("/api/v1/safetymonitor/0/description")
def description():
    with safety.state_lock:
        desc = safety.current_status_text

    return {
        "Value": desc,
        "ErrorNumber": 0,
        "ErrorMessage": ""
    }


@app.get("/api/v1/safetymonitor/0/connected")
def connected():
    return {
        "Value": True,
        "ErrorNumber": 0,
        "ErrorMessage": ""
    }


@app.get("/api/v1/safetymonitor/0/interfaceversion")
def interfaceversion():
    return {
        "Value": 2,
        "ErrorNumber": 0,
        "ErrorMessage": ""
    }


@app.get("/api/v1/safetymonitor/0/driverversion")
def driverversion():
    return {
        "Value": "1.5.0",
        "ErrorNumber": 0,
        "ErrorMessage": ""
    }


@app.get("/api/v1/safetymonitor/0/driverinfo")
def driverinfo():
    return {
        "Value": "Meteo Alpaca Safety Monitor",
        "ErrorNumber": 0,
        "ErrorMessage": ""
    }


@app.get("/api/v1/safetymonitor/0/supportedactions")
def supportedactions():
    return {
        "Value": [],
        "ErrorNumber": 0,
        "ErrorMessage": ""
    }


@app.get("/api/v1/safetymonitor/0/devicestate")
def devicestate():
    return {
        "Value": [],
        "ErrorNumber": 0,
        "ErrorMessage": ""
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=11112
    )
