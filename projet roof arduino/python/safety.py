import os
import sys
import time
import threading
import requests

from datetime import datetime

LAT = "48.119722"
LON = "-1.200556"

MAX_WIND_SPEED = 40.0
MAX_RAIN_PROB = 30
MAX_RAIN_MM = 0.1
MAX_CLOUD_COVER = 80
MAX_TEMP_MIN = 0.5

CACHE_TIMEOUT_MINUTES = 30


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

LOG_FILE = os.path.join(
    DATA_DIR,
    "meteo_log.txt"
)

is_safe = False

current_status_text = "Initialisation..."

state_lock = threading.Lock()

monitor_started = False

last_weather_update = None

last_good_timestamp = None

last_good_data = None

weather_data = {
    "wind": 0,
    "clouds": 0,
    "rain_prob": 0,
    "rain_mm": 0,
    "temperature": 0
}


def get_last_update():

    if last_weather_update is None:
        return "Never"

    return last_weather_update.strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def write_to_log(message):

    now = datetime.now()

    timestamp = now.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    try:

        lines = []

        try:

            with open(
                LOG_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                for line in f:

                    try:

                        if line.startswith("["):

                            date_str = line[1:20]

                            log_date = datetime.strptime(
                                date_str,
                                "%Y-%m-%d %H:%M:%S"
                            )

                            age = (
                                now - log_date
                            ).total_seconds()

                            if age <= 48 * 3600:

                                lines.append(line)

                    except Exception:
                        pass

        except FileNotFoundError:
            pass

        lines.insert(
            0,
            f"[{timestamp}] {message}\n"
        )

        with open(
            LOG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            f.writelines(lines)

    except Exception as ex:

        print(
            f"Erreur log météo : {ex}"
        )


def update_weather_data(data):

    global is_safe
    global current_status_text
    global last_weather_update
    global last_good_data
    global last_good_timestamp

    current = data.get(
        "current",
        {}
    )

    curr_temp = current.get(
        "temperature_2m",
        0
    )

    curr_wind = current.get(
        "wind_speed_10m",
        0
    )

    curr_clouds = current.get(
        "cloud_cover",
        0
    )

    hourly = data.get(
        "hourly",
        {}
    )

    times = hourly.get(
        "time",
        []
    )

    precip_prob = hourly.get(
        "precipitation_probability",
        []
    )

    precip = hourly.get(
        "precipitation",
        []
    )

    hourly_temps = hourly.get(
        "temperature_2m",
        []
    )

    current_hour_str = datetime.now().strftime(
        "%Y-%m-%dT%H:00"
    )

    try:

        current_index = times.index(
            current_hour_str
        )

    except ValueError:

        current_index = 0

    next_index = min(
        current_index + 1,
        len(times) - 1
    )

    next_rain_prob = (
        precip_prob[next_index]
        if next_index < len(precip_prob)
        else 0
    )

    next_rain = (
        precip[next_index]
        if next_index < len(precip)
        else 0
    )

    next_temp = (
        hourly_temps[next_index]
        if next_index < len(hourly_temps)
        else 0
    )

    weather_data["wind"] = curr_wind
    weather_data["clouds"] = curr_clouds
    weather_data["rain_prob"] = next_rain_prob
    weather_data["rain_mm"] = next_rain
    weather_data["temperature"] = curr_temp

    reasons = []

    if (
        next_rain_prob > MAX_RAIN_PROB
        or next_rain > MAX_RAIN_MM
    ):
        reasons.append(
            f"PLUIE ({next_rain_prob}%)"
        )

    if curr_wind > MAX_WIND_SPEED:
        reasons.append(
            f"VENT ({curr_wind}km/h)"
        )

    if curr_clouds > MAX_CLOUD_COVER:
        reasons.append(
            f"NUAGES ({curr_clouds}%)"
        )

    if (
        curr_temp <= MAX_TEMP_MIN
        or next_temp <= MAX_TEMP_MIN
    ):
        reasons.append(
            "RISQUE GEL"
        )

    weather_summary = (
        f"Temp={curr_temp}°C | "
        f"Vent={curr_wind} km/h | "
        f"Nuages={curr_clouds}% | "
        f"Pluie={next_rain_prob}% "
        f"({next_rain} mm)"
    )

    with state_lock:

        if reasons:

            is_safe = False

            current_status_text = (
                f"UNSAFE [{', '.join(reasons)}] | "
                f"{weather_summary}"
            )

        else:

            is_safe = True

            current_status_text = (
                f"SAFE | {weather_summary}"
            )

        last_weather_update = datetime.now()

        last_good_timestamp = datetime.now()

        last_good_data = data


def weather_monitor_loop():

    global is_safe
    global current_status_text

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}"
        f"&longitude={LON}"
        f"&current=temperature_2m,"
        f"relative_humidity_2m,"
        f"wind_speed_10m,"
        f"cloud_cover"
        f"&hourly=precipitation_probability,"
        f"precipitation,"
        f"temperature_2m"
        f"&wind_speed_unit=kmh"
        f"&timezone=Europe%2FParis"
        f"&forecast_days=1"
    )

    while True:

        try:

            response = None

            for attempt in range(3):

                try:

                    response = requests.get(
                        url,
                        timeout=10
                    )

                    break

                except Exception:

                    write_to_log(
                        f"ERREUR RESEAU "
                        f"TENTATIVE {attempt + 1}/3"
                    )

                    time.sleep(5)

            if response is None:

                raise Exception(
                    "Open-Meteo inaccessible"
                )

            data = response.json()

            update_weather_data(data)

            write_to_log(
                current_status_text
            )

        except Exception as ex:

            cache_used = False

            if last_good_timestamp:

                age = (
                    datetime.now()
                    - last_good_timestamp
                ).total_seconds() / 60

                if age <= CACHE_TIMEOUT_MINUTES:

                    cache_used = True

                    current_status_text = (
                        f"SAFE | CACHE UTILISE "
                        f"({int(age)} min)"
                    )

                    write_to_log(
                        current_status_text
                    )

            if not cache_used:

                with state_lock:

                    is_safe = False

                    current_status_text = (
                        f"UNSAFE | {ex}"
                    )

                write_to_log(
                    current_status_text
                )

        time.sleep(600)


def start_weather_monitor():

    global monitor_started

    if monitor_started:
        return

    threading.Thread(
        target=weather_monitor_loop,
        daemon=True
    ).start()

    monitor_started = True