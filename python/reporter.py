
import time
import copy
import requests
import urllib3
import threading
from context import Context


class Reporter:
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._started = False
        self._stop = False
        self._stop_lock = threading.Lock()

    def start(self):
        if self._started:
            return

        self._started = True
        self._stop = False
        self._thread = threading.Thread(target=self.loop, args=(copy.deepcopy(Context().data),))
        self._thread.start()

    def stop(self):
        if not self._started:
            return

        with self._stop_lock:
            self._stop = True
        self._thread.join()
        self._started = False
        self._stop = False

    def loop(self, data):
        while True:
            time.sleep(2.9)

            try:
                self.send_status(data)
            except Exception:
                pass

            stop = False
            with self._stop_lock:
                stop = self._stop
            if stop:
                break

    def send_status(self, data):
        status = Context().webdriver.get_current_status()
        if status is None:
            status = {
                "_type": "EMPTY"
            }
        else:
            status["_type"] = "DATA"
        requests.post(data.tg_bot_url, json=status, verify=False)
