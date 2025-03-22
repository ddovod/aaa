
from selenium import webdriver
from selenium.webdriver.common.by import By


def exists(driver, by, path):
    return len(driver.find_elements(by, path)) != 0

def visible(driver, by, path):
    return driver.find_element(by, path).is_displayed()

def get(driver, by, path):
    return driver.find_element(by, path)

def get_if_visible(driver, by, path):
    els = driver.find_elements(by, path)
    if len(els) == 1:
        el = els[0]
        if el.is_displayed():
            return el
    elif len(els) > 1:
        log.warning("Several '" + path + "' found")
    return None

