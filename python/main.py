
import time
import traceback
from selenium import webdriver
from log import log
from gui import Gui
from context import Context
from config import Config
from playsound import playsound


def init_context():
    config = Config()
    Context().set_config(config)

    data = config.data()
    Context().set_data(data)
    
    gui = Gui()
    Context().set_gui(gui)


def main():
    init_context()
    gui = Context().gui()
    while not gui.should_close():
        gui.update()
    gui.terminate()
    log.info('Terminating, OK')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.error(traceback.format_exc())
        # while True:
        #     playsound('alarm.wav')
