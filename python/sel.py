
from selenium import webdriver
from selenium.webdriver.common.by import By


def exists(driver, by, path):
    return len(driver.find_elements(by, path)) != 0

def visible(driver, by, path):
    return driver.find_element(by, path).is_displayed()

def get(driver, by, path):
    return driver.find_element(by, path)

def get_if_visible(driver, by, path):
    bid_buttons = driver.find_elements(By.ID, 'addAuctionBidButton')
    if len(bid_buttons) == 1:
        bid_button = bid_buttons[0]
        if bid_button.is_displayed():

