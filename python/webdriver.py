
import time
import threading
import copy
import json
import sel
import events
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from log import log
from context import Context
from data import Data


class WebDriver:
    def __init__(self):
        self._stop = False
        self._stop_lock = threading.Lock()
        self._started = False
        self._out_events = []
        self._out_events_lock = threading.Lock()
        self._browser_window_pos_x = 0
        self._browser_window_pos_y = 0
        self._browser_window_width = 0
        self._browser_window_height = 0
        self._current_status = None
        self._current_status_lock = threading.Lock()

    def start(self):
        if self._started:
            return

        self._started = True
        self._stop = False
        self._loop_data = {}
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
        self._loop_data = {}
        with self._current_status_lock:
            self._current_status = None

    def get_and_clear_events(self):
        result = None
        with self._out_events_lock:
            result = self._out_events
            self._out_events = []
        return result

    def get_current_status(self):
        result = None
        with self._current_status_lock:
            if self._current_status is not None:
                result = copy.deepcopy(self._current_status)
        return result

    def report_browser_window_geometry_if_needed(self, driver):
        pos = driver.get_window_position()
        x = pos.get('x')
        y = pos.get('y')

        size = driver.get_window_size()
        width = size.get("width")
        height = size.get("height")

        if x != self._browser_window_pos_x or y != self._browser_window_pos_y or width != self._browser_window_width or height != self._browser_window_height:
            self._browser_window_pos_x = x
            self._browser_window_pos_y = y
            self._browser_window_width = width
            self._browser_window_height = height
            with self._out_events_lock:
                self._out_events.append(events.ReportBrowserWindowGeometry(x, y, width, height))

    def update(self):
        evs = self.get_and_clear_events()
        for event in evs:
            if isinstance(event, events.ReportBrowserWindowGeometry):
                old_geom = Context().data.browser_window_geometry
                new_geom = event.browser_window_geometry
                if old_geom.pos_x != new_geom.pos_x or old_geom.pos_y != new_geom.pos_y or old_geom.size_x != new_geom.size_x or old_geom.size_y != new_geom.size_y:
                    Context().data.browser_window_geometry = event.browser_window_geometry
                    Context().config.save()

    def loop(self, data):
        log.debug('Starting webdriver loop')
        
        options = webdriver.ChromeOptions()
        options.debugger_address = '127.0.0.1:54323'
        driver = webdriver.Chrome(options=options)
        driver.switch_to.new_window('window')
        geom = data.browser_window_geometry
        if geom.pos_x >= 0 and geom.pos_y >= 0:
            driver.set_window_position(geom.pos_x, geom.pos_y)
        if geom.size_x >= 0 and geom.size_y >= 0:
            driver.set_window_size(geom.size_x, geom.size_y)

        while True:
            time.sleep(1)

            try:
                self.run_iter(driver, data)
            except Exception:
                pass
            self.report_browser_window_geometry_if_needed(driver)

            stop = False
            with self._stop_lock:
                stop = self._stop
            if stop:
                break

        driver.close()
        driver.quit()
        log.debug('Finishing webdriver loop')

    def run_iter(self, driver, data):
        # log.debug('Making iter with data:')
        # log.debug(json.dumps(data.to_json(), indent=2))

        if 'lastRefreshTimestamp' not in self._loop_data:
            self._loop_data['lastRefreshTimestamp'] = time.time()
            driver.get(data.trade_url)

        current_url = driver.current_url

        # Checking if we're still on the trades page
        if current_url == data.trade_url:
            # Updating the page by timer
            now_secs = time.time()
            if now_secs - self._loop_data['lastRefreshTimestamp'] >= data.seconds_refresh:
                log.debug('Refreshing after ' + str(now_secs - self._loop_data['lastRefreshTimestamp']) + ' seconds')
                self._loop_data['lastRefreshTimestamp'] = now_secs
                driver.get(data.trade_url)

            # Checking bid button visibility
            bid_btn = sel.get_if_visible(driver, By.ID, 'addAuctionBidButton')
            if bid_btn != None:
                # Making a bid
                bid_btn.click()
                time.sleep(2)

                # Check for error
                close_error_btn = sel.get_if_visible(driver, By.XPATH, data.close_bid_error_btn_xpath)
                if close_error_btn != None:
                    log.info('Close error button is visible')
                    # Close error popup
                    close_error_btn.click()
                    time.sleep(1)

                    # Close bid popup
                    close_bid_btn = sel.get_if_visible(driver, By.XPATH, data.close_bid_btn_xpath)
                    if close_bid_btn != None:
                        log.info('Close button is visible')
                        close_bid_btn.click()
                        time.sleep(1)
                    else:
                        log.info('Close button is NOT visible')
                else:
                    log.info('Close error button is NOT visible')
            else:
                lot_statuses = []
                for lot in data.lots:
                    if sel.get_if_visible(driver, By.ID, 'addAuctionBidButton') != None:
                        break

                    time_left, time_left_text = sel.get_time_seconds_if_exists(driver, By.XPATH, lot.time_left_xpath)
                    my_bid, my_bid_txt = sel.get_bid_if_exists(driver, By.XPATH, lot.my_bid_xpath)
                    best_bid, best_bid_txt = sel.get_bid_if_exists(driver, By.XPATH, lot.best_bid_xpath)
                    # log.info(str(time_left) + '  ' + str(my_bid) + '  ' + str(best_bid))

                    if time_left_text != None and my_bid_txt != None and best_bid_txt != None:
                        lot_statuses.append({
                            "time_left_str": time_left_text,
                            "best_bid": best_bid_txt,
                            "my_bid": my_bid_txt,
                            "time_left_min_str": self.to_hms_str(lot.seconds_left_min)
                        })

                    if time_left != None and my_bid != None and best_bid != None and time_left < lot.seconds_left_min and my_bid < best_bid:
                        open_bid_btn = sel.get_if_visible(driver, By.XPATH, lot.open_bid_btn_xpath)
                        if open_bid_btn != None:
                            open_bid_btn.click()
                            time.sleep(2)

                # Save status if everything is ok
                if len(lot_statuses) == len(data.lots):
                    with self._current_status_lock:
                        self._current_status = {
                            "lots": lot_statuses,
                            "time": time.time()
                        }
        else:
            # TODO: handle login
            pass

    def to_hms_str(self, seconds):
        hours = seconds // (60 * 60)
        seconds %= (60 * 60)
        minutes = seconds // 60
        seconds %= 60
        return "%02i:%02i:%02i" % (hours, minutes, seconds)

