import time

import pythoncom
import win32com.client

from logger import log
from config import TELESCOPE_DRIVER

PARK_TIMEOUT = 300


def ensure_mount_parked():

    pythoncom.CoInitialize()

    try:

        print("================================")
        print("ensure_mount_parked()")
        print("================================")

        print(
            f"Driver : {TELESCOPE_DRIVER}"
        )

        telescope = win32com.client.Dispatch(
            TELESCOPE_DRIVER
        )

        print("Driver loaded")

        telescope.Connected = True

        print(
            f"Connected : {telescope.Connected}"
        )

        print(
            f"AtPark : {telescope.AtPark}"
        )

        if telescope.AtPark:

            print(
                "Mount already parked"
            )

            log(
                "Mount already parked"
            )

            return True

        print(
            "Mount not parked"
        )

        log(
            "Mount not parked"
        )

        print(
            "Sending Park()"
        )

        log(
            "Sending PARK command"
        )

        telescope.Park()

        timeout = (
            time.time()
            + PARK_TIMEOUT
        )

        while time.time() < timeout:

            print(
                "Waiting for park..."
            )

            if telescope.AtPark:

                print(
                    "Mount parked"
                )

                log(
                    "Mount parked"
                )

                return True

            time.sleep(2)

        print(
            "Parking timeout"
        )

        log(
            "Parking timeout"
        )

        return False

    except Exception as ex:

        print(
            f"EQMOD exception: {ex}"
        )

        log(
            f"EQMOD error: {ex}"
        )

        return False

    finally:

        pythoncom.CoUninitialize()