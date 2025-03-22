
import re
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_if_visible(driver, by, path):
    try:
        els = driver.find_elements(by, path)
        if len(els) == 1:
            el = els[0]
            if el.is_displayed():
                return el
        elif len(els) > 1:
            log.warning("Several '" + path + "' found")
    except Exception:
        pass

    return None


def get_bid_if_exists(driver, by, path):
    try:
        bid_txt = get_if_visible(driver, by, path)
        if bid_txt != None:
            return int(re.sub("[^0-9]", "", bid_txt.text))
    except Exception:
        pass

    return None


def get_time_seconds_if_exists(driver, by, path):
    try:
        time_left_txt = get_if_visible(driver, by, path)
        if time_left_txt != None:
            hms = time_left_txt.text
            if hms != None:
                comps = hms.split(':')
                if len(comps) == 3:
                    return int(comps[0]) * 60 * 60 + int(comps[1]) * 60 + int(comps[2])
    except Exception:
        pass

    return None

