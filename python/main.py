
import time
import traceback
from selenium import webdriver
from log import log
from gui import Gui
from context import Context
from config import Config
from playsound import playsound
from webdriver import WebDriver
from reporter import Reporter


def init_context():
    Context().config = Config()
    Context().data = Context().config.data()
    Context().gui = Gui()
    Context().webdriver = WebDriver()
    Context().reporter = Reporter()


def main():
    init_context()
    gui = Context().gui
    driver = Context().webdriver
    reporter = Context().reporter
    reporter.start()
    while not gui.should_close():
        gui.update()
        driver.update()
    reporter.stop()
    gui.terminate()
    log.info('Terminating, OK')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.error(traceback.format_exc())
        # while True:
        #     playsound('alarm.wav')
