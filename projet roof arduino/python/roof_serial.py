import serial
import threading


class RoofController:

    def __init__(self, port, baudrate):

        self.lock = threading.Lock()

        self.ser = serial.Serial(
            port,
            baudrate,
            timeout=2
        )

    def send(self, cmd):

        with self.lock:

            self.ser.reset_input_buffer()

            self.ser.write(
                f"{cmd}\n".encode()
            )

            return (
                self.ser.readline()
                .decode()
                .strip()
            )

    def open(self):
        return self.send("OPEN")

    def close(self):
        return self.send("CLOSE")

    def stop(self):
        return self.send("STOP")

    def status(self):
        return self.send("STATUS")