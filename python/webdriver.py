
import time
import threading
import copy
import json
import undetected_chromedriver as uc
from selenium import webdriver
from log import log
from context import Context


class WebDriver:
    def __init__(self):
        self._stop = False;
        self._started = False
        self._lock = threading.Lock()

    def start(self):
        self._started = True
        self._stop = False
        self._loop_data = {}
        self._thread = threading.Thread(target=self.loop, args=(copy.deepcopy(Context().data),))
        self._thread.start()

    def stop(self):
        with self._lock:
            self._stop = True
        self._thread.join()
        self._started = False
        self._stop = False
        self._loop_data = {}

    def loop(self, data):
        log.debug('Starting webdriver loop')
        
        options = webdriver.ChromeOptions()
        options.debugger_address = '127.0.0.1:54323'
        driver = webdriver.Chrome(options=options)
        driver.switch_to.new_window('window')

        while True:
            time.sleep(1)

            self.run_iter(driver, data);

            stop = False
            with self._lock:
                stop = self._stop
            if stop:
                break

        driver.close()
        driver.quit()
        log.debug('Finishing webdriver loop')

    def run_iter(self, driver, data):
        log.debug('Making iter with data:')
        log.debug(json.dumps(data.to_json(), indent=2))

        if 'lastRefreshTimestamp' not in self._loop_data:
            self._loop_data['lastRefreshTimestamp'] = time.time()
            driver.get(data.trade_url)

        current_url = driver.current_url
        if current_url == data.trade_url:
            now_secs = time.time()
            if now_secs - self._loop_data['lastRefreshTimestamp'] >= data.seconds_refresh:
                log.debug('Refreshing after ' + str(now_secs - self._loop_data['lastRefreshTimestamp']) + ' seconds')
                self._loop_data['lastRefreshTimestamp'] = now_secs
                driver.get(data.trade_url)
            
        else:
            # TODO: handle login
            pass
