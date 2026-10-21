import falcon
from wsgiref.simple_server import make_server
import safety
import threading

app = falcon.App()

# Routes du Safety Monitor
app.add_route('/api/v1/safetymonitor/0/issafe', safety.issafe())
app.add_route('/api/v1/safetymonitor/0/name', safety.name())
app.add_route('/api/v1/safetymonitor/0/description', safety.description())
app.add_route('/api/v1/safetymonitor/0/connected', safety.connected())
app.add_route('/api/v1/safetymonitor/0/connect', safety.connect())
app.add_route('/api/v1/safetymonitor/0/disconnect', safety.disconnect())
app.add_route('/api/v1/safetymonitor/0/connecting', safety.connecting())
app.add_route('/api/v1/safetymonitor/0/interfaceversion', safety.interfaceversion())
app.add_route('/api/v1/safetymonitor/0/driverversion', safety.driverversion())
app.add_route('/api/v1/safetymonitor/0/driverinfo', safety.driverinfo())
app.add_route('/api/v1/safetymonitor/0/supportedactions', safety.supportedactions())
app.add_route('/api/v1/safetymonitor/0/devicestate', safety.devicestate())

if __name__ == '__main__':
    # Lancement du thread de météo en arrière-plan
    monitor_thread = threading.Thread(target=safety.weather_monitor_loop, daemon=True)
    monitor_thread.start()

    print("Démarrage du serveur Safety Monitor (Météo)...")
    print("En écoute sur le port 11112")
    with make_server('0.0.0.0', 11112, app) as httpd:
        print("Serveur Safety Monitor prêt !")
        httpd.serve_forever()