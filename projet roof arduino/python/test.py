import win32com.client
import time

scope = win32com.client.Dispatch(
    "EQMOD_SIM.Telescope"
)

scope.Connected = True

print("AtPark avant :", scope.AtPark)

scope.Unpark()

time.sleep(2)

print("AtPark après Unpark :", scope.AtPark)

scope.Park()

while not scope.AtPark:
    print("Parking...")
    time.sleep(1)

print("Monture parkée")