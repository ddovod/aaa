
import time
import threading
import copy
import json
import sel
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
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

        return

        current_url = driver.current_url
        if current_url == data.trade_url:
            # Updating the page by timer
            now_secs = time.time()
            if now_secs - self._loop_data['lastRefreshTimestamp'] >= data.seconds_refresh:
                log.debug('Refreshing after ' + str(now_secs - self._loop_data['lastRefreshTimestamp']) + ' seconds')
                self._loop_data['lastRefreshTimestamp'] = now_secs
                driver.get(data.trade_url)

            # Checking bid button visibility
            bid_buttons = driver.find_elements(By.ID, 'addAuctionBidButton')
            if len(bid_buttons) == 1:
                bid_button = bid_buttons[0]
                if bid_button.is_displayed():
                    # Making a bid
                    # bid_button.click()
                    time.sleep(2)

                    # Check for error
                    close_error_buttons = driver.find_elements(By.XPATH, data.close_bid_error_btn_xpath);
                    if len(close_error_buttons) == 1:
                        close_error_button = close_error_buttons[0]
                        if close_error_button.is_displayed():
                            # Close error popup
                            close_error_button.click()
                            time.sleep(1)
                            
                    elif len(close_error_buttons) > 1:
                        log.warning("Several close_bid_error_btn_xpath elements found")
            elif len(bid_buttons) > 1:
                log.warning("Several addAuctionBidButton elements found")

                    

                    # var btnEl = document.evaluate(${closeErrorBtnXpath}, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; return btnEl != null && btnEl.checkVisibility();
                
            # if len(driver.find_elements(By.ID, 'addAuctionBidButton')) == 0:
            # if len(driver.find_elements(By.XPATH, '//*[@id="main-segment"]/div[3]/div/div[1]/div/div[1]/div/button')) == 0:
            #     log.error('Not found')
            # else:
            #     log.error('Found')
            # log.debug("Post find")
        else:
            # TODO: handle login
            pass
