from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as exception
import csv
import pandas as pd
import time


def get_prod_page_details(link):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(link)
    # driver.minimize_window()
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div/div/div/section/div[2]/button[1]")))

    cookie_alert = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div/div/section/div[2]/button[1]")
    action = ActionChains(driver)
    action.click(on_element=cookie_alert)
    action.perform()

    # time.sleep(1)

    # following codes are commented out and kept here, potentially for extracting information from incredients, nutrition and product details sections

    # wait.until(EC.presence_of_element_located((By.ID, "ingredients-title")))
    # ingredients_button = driver.find_element_by_id("ingredients-title")

    # wait.until(EC.presence_of_element_located((By.ID, "nutrition-title")))
    # nutrition_button = driver.find_element_by_id("nutrition-title")

    # wait.until(EC.presence_of_element_located((By.ID, "productDetails-title")))
    # proddetails_button = nutrition_button = driver.find_element_by_id("productDetails-title")

    # action = ActionChains(driver)
    # action.click(on_element = ingredients_button)
    # action.perform()
    # wait.until(EC.presence_of_element_located((By.ID, "ingredients-region")))

    # action = ActionChains(driver)

    # action.click(on_element = nutrition_button)
    # action.perform()
    # wait.until(EC.presence_of_element_located((By.ID, "nutrition-region")))

    # action = ActionChains(driver)
    # action.click(on_element = proddetails_button)
    # action.perform()

    try:
        wait.until(EC.presence_of_element_located(
            (By.ID, "productDescription")))
        prod_desc = driver.find_element_by_id("productDescription").text
    except:
        prod_desc = ''

    try:
        wait.until(EC.presence_of_element_located(
            (By.ID, "marketingDescriptionBop")))
        mktg_desc = driver.find_element_by_id("marketingDescriptionBop").text
    except:
        mktg_desc = ''

    try:
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "offerDescription___1A6Ew.underline___2kMYl")))
        offer = driver.find_element_by_class_name(
            "offerDescription___1A6Ew.underline___2kMYl").text
    except:
        offer = ''
    driver.quit()

    return prod_desc, mktg_desc, offer
