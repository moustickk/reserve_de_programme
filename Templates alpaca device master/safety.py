# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# safety.py - Safety Monitor Météo (Open-Meteo)
# Version avec journalisation dans meteo_log.txt
# -----------------------------------------------------------------------------

import json
import time
import threading
import requests
from datetime import datetime

# --- CONFIGURATION GÉOGRAPHIQUE (Vitré) ---
LAT = "48.119722"
LON = "-1.200556"

# --- SEUILS DE SÉCURITÉ ---
MAX_WIND_SPEED = 40.0      # Vitesse max du vent en km/h
MAX_RAIN_PROB = 30         # Probabilité de pluie max en %
MAX_RAIN_MM = 0.1          # Quantité de pluie max en mm
MAX_CLOUD_COVER = 80       # Couverture nuageuse max en %
MAX_TEMP_MIN = 0.5         # Température minimale (gel)

# --- FICHIER LOG ---
LOG_FILE = "meteo_log.txt"

# --- ETAT GLOBAL ---
is_safe = False            
current_status_text = "Initialisation..."
state_lock = threading.Lock()

# --- GESTION DES RÉPONSES ALPACA ---
class PropertyResponse:
    def __init__(self, value, req, err=None):
        self.value = value
        self.req = req
        self.err = err
    @property
    def json(self):
        trans_id = int(self.req.params.get('ClientTransactionID', 0)) if hasattr(self.req, 'params') else 0
        if self.err:
            return json.dumps({"ErrorNumber": 1024, "ErrorMessage": str(self.err), "ClientTransactionID": trans_id})
        return json.dumps({"Value": self.value, "ErrorNumber": 0, "ErrorMessage": "", "ClientTransactionID": trans_id})

class MethodResponse:
    def __init__(self, req, err=None):
        self.req = req
        self.err = err
    @property
    def json(self):
        trans_id = int(self.req.params.get('ClientTransactionID', 0)) if hasattr(self.req, 'params') else 0
        if self.err:
            return json.dumps({"ErrorNumber": 1024, "ErrorMessage": str(self.err), "ClientTransactionID": trans_id})
        return json.dumps({"ErrorNumber": 0, "ErrorMessage": "", "ClientTransactionID": trans_id})

# --- FONCTION D'ÉCRITURE DANS LE LOG ---
def write_to_log(message):
    """
    Écrit un message avec horodatage dans le fichier log.
    Les entrées les plus récentes sont placées en haut.
    Conserve uniquement les 48 dernières heures.
    """

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    try:
        lines = []

        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        if line.startswith("["):
                            date_str = line[1:20]
                            log_date = datetime.strptime(
                                date_str,
                                "%Y-%m-%d %H:%M:%S"
                            )

                            age_seconds = (now - log_date).total_seconds()

                            if age_seconds <= 48 * 3600:
                                lines.append(line)

                    except Exception:
                        pass

        except FileNotFoundError:
            pass

        # Nouvelle ligne en PREMIERE position
        lines.insert(0, f"[{timestamp}] {message}\n")

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)

    except Exception as e:
        print(f"Impossible d'écrire dans le log : {e}")

# --- THREAD DE SURVEILLANCE MÉTÉO (OPEN-METEO) ---
def weather_monitor_loop():
    global is_safe, current_status_text
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,cloud_cover&hourly=precipitation_probability,precipitation,temperature_2m&wind_speed_unit=kmh&timezone=Europe%2FParis&forecast_days=1"
    
    while True:
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                current = data.get('current', {})
                curr_temp = current.get('temperature_2m', 0)
                curr_hum = current.get('relative_humidity_2m', 0)
                curr_wind = current.get('wind_speed_10m', 0)
                curr_clouds = current.get('cloud_cover', 0)
                
                hourly = data.get('hourly', {})
                times = hourly.get('time', [])
                precip_prob = hourly.get('precipitation_probability', [])
                precip = hourly.get('precipitation', [])
                hourly_temps = hourly.get('temperature_2m', [])
                
                now = datetime.now()
                current_hour_str = now.strftime("%Y-%m-%dT%H:00")
                
                try:
                    current_index = times.index(current_hour_str)
                except ValueError:
                    current_index = 0
                
                next_index = current_index + 1
                if next_index >= len(times):
                    next_index = current_index
                
                next_rain_prob = precip_prob[next_index] if next_index < len(precip_prob) else 0
                next_rain = precip[next_index] if next_index < len(precip) else 0
                next_temp = hourly_temps[next_index] if next_index < len(hourly_temps) else 0
                
                reasons = []
                if next_rain_prob > MAX_RAIN_PROB or next_rain > MAX_RAIN_MM:
                    reasons.append(f"PLUIE PRÉVUE ({next_rain_prob}%)")
                if curr_wind > MAX_WIND_SPEED:
                    reasons.append(f"VENT ACTUEL ({curr_wind}km/h)")
                if curr_clouds > MAX_CLOUD_COVER:
                    reasons.append(f"NUAGES ACTUELS ({curr_clouds}%)")
                if curr_temp <= MAX_TEMP_MIN or next_temp <= MAX_TEMP_MIN:
                    reasons.append(f"RISQUE DE GEL")
                
                status_details = (
                    f"Actuel: {curr_temp}°C, Vent {curr_wind}km/h, Nuages {curr_clouds}% | "
                    f"Prévisions +1h: Pluie {next_rain_prob}% ({next_rain}mm), T {next_temp}°C"
                )
                
                with state_lock:
                    if reasons:
                        is_safe = False
                        current_status_text = f"UNSAFE [{', '.join(reasons)}] | {status_details}"
                    else:
                        is_safe = True
                        current_status_text = f"SAFE | {status_details}"
                    
                    # Écriture dans le log à chaque cycle
                    log_status = "SAFE" if is_safe else "UNSAFE"
                    write_to_log(f"{log_status} | {current_status_text}")
                    
            else:
                with state_lock:
                    is_safe = False
                    current_status_text = f"UNSAFE | Erreur API HTTP: {response.status_code}"
                    write_to_log(f"ERREUR API | {current_status_text}")
                    
        except Exception as e:
            with state_lock:
                is_safe = False
                current_status_text = f"UNSAFE | Erreur réseau: {e}"
                write_to_log(f"ERREUR RESEAU | {current_status_text}")
        
        time.sleep(600) # 10 minutes

# --- ROUTES ALPACA ---

class issafe:
    def on_get(self, req, resp):
        with state_lock:
            val = is_safe
        resp.text = PropertyResponse(val, req).json

class name:
    def on_get(self, req, resp):
        resp.text = PropertyResponse("Meteo Safety Monitor (Open-Meteo)", req).json

class description:
    def on_get(self, req, resp):
        with state_lock:
            reason = current_status_text
        resp.text = PropertyResponse(reason, req).json

class connected:
    def on_get(self, req, resp): resp.text = PropertyResponse(True, req).json
    def on_put(self, req, resp): resp.text = MethodResponse(req).json

class connect:
    def on_put(self, req, resp): resp.text = MethodResponse(req).json

class disconnect:
    def on_put(self, req, resp): resp.text = MethodResponse(req).json

class connecting:
    def on_get(self, req, resp): resp.text = PropertyResponse(False, req).json

class interfaceversion:
    def on_get(self, req, resp): resp.text = PropertyResponse(2, req).json

class driverversion:
    def on_get(self, req, resp): resp.text = PropertyResponse("1.4.0", req).json

class driverinfo:
    def on_get(self, req, resp): resp.text = PropertyResponse("Meteo Alpaca Safety Monitor", req).json

class supportedactions:
    def on_get(self, req, resp): resp.text = PropertyResponse([], req).json

class devicestate:
    def on_get(self, req, resp): resp.text = PropertyResponse([], req).json

# --- FONCTIONS NON SUPPORTÉES ---
class action:
    def on_put(self, req, resp): resp.text = MethodResponse(req, NotImplementedException()).json
class commandblind:
    def on_put(self, req, resp): resp.text = MethodResponse(req, NotImplementedException()).json
class commandbool:
    def on_put(self, req, resp): resp.text = MethodResponse(req, NotImplementedException()).json
class commandstring:
    def on_put(self, req, resp): resp.text = MethodResponse(req, NotImplementedException()).json
class NotImplementedException(Exception): pass