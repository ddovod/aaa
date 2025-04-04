
import json
import time
import copy
import requests
import traceback
import urllib3
import threading
from log import log
from context import Context


class Reporter:
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._started = False
        self._stop = False
        self._stop_lock = threading.Lock()
        self._last_report_status_time = 0.0

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
            except Exception as e:
                log.error(traceback.format_exc())

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
            status_code = requests.post(data.tg_bot_url, json=status).status_code
            log.info('POST (EMPTY) response code: ' + str(status_code))
        elif 'time' in status and status['time'] > self._last_report_status_time:
            self._last_report_status_time = status['time']
            status["_type"] = "DATA"
            status_code = requests.post(data.tg_bot_url, json=status).status_code
            log.info('POST (DATA) response code: ' + str(status_code))
        else:
            log.info('Status is not updated, skipping')
