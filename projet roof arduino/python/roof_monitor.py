import threading
import time


class RoofMonitor:

    def __init__(self, sync_func):

        self.sync_func = sync_func

        self.thread = threading.Thread(
            target=self.run,
            daemon=True
        )

    def start(self):

        self.thread.start()

    def run(self):

        while True:

            try:
                self.sync_func()

            except Exception as ex:
                print(ex)

            time.sleep(1)