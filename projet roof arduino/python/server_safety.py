from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

import safety


@asynccontextmanager
async def lifespan(app: FastAPI):

    safety.start_weather_monitor()

    yield


app = FastAPI(lifespan=lifespan)


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
        "Value": "2.0.0",
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

    with safety.state_lock:

        age = -1

        if safety.last_weather_update:

            age = int(
                (
                    safety.datetime.now()
                    - safety.last_weather_update
                ).total_seconds() / 60
            )

        result = [
            {
                "Name": "IsSafe",
                "Value": safety.is_safe
            },
            {
                "Name": "Wind",
                "Value": safety.weather_data["wind"]
            },
            {
                "Name": "CloudCover",
                "Value": safety.weather_data["clouds"]
            },
            {
                "Name": "RainProbability",
                "Value": safety.weather_data["rain_prob"]
            },
            {
                "Name": "RainMM",
                "Value": safety.weather_data["rain_mm"]
            },
            {
                "Name": "Temperature",
                "Value": safety.weather_data["temperature"]
            },
            {
                "Name": "LastWeatherUpdate",
                "Value": safety.get_last_update()
            },
            {
                "Name": "DataAgeMinutes",
                "Value": age
            },
            {
                "Name": "WeatherSource",
                "Value": "Open-Meteo"
            }
        ]

    return {
        "Value": result,
        "ErrorNumber": 0,
        "ErrorMessage": ""
    }


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=11112
    )