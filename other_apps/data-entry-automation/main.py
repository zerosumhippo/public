from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time

GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSeD09ZU6CkIm_Fl1Q89Izzu5O_FJCOCJ0uisp25s5WCW5gwgQ" \
                   "/viewform?usp=sf_link"
APT_SEARCH_LINK = "https://leasingkc.com/listings/bedrooms_1/apartment/kansas-city,-mo+downtown+plaza+westport/"


def get_apt_listings():
    response = requests.get(url=APT_SEARCH_LINK)
    apt_page = response.text
    soup = BeautifulSoup(apt_page, "html.parser")
    apt_listings = soup.select(selector=".result-list ul li .listing-location a")
    apt_prices = soup.select(selector=".result-list ul li .listing-info p")
    listing_links = [listing.get("href") for listing in apt_listings]
    listing_addrs = [listing.get_text().strip().replace("\n", ", ") for listing in apt_listings]
    listing_prices = [price.get_text().strip() for price in apt_prices]
    listing_dict = {
        "links": listing_links,
        "addresses": listing_addrs,
        "prices": listing_prices,
    }
    return listing_dict


def fill_in_form(input_data):
    chrome_driver_path = "C:/Users/breim/Development/chromedriver.exe"
    service = Service(f"r{chrome_driver_path}")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(GOOGLE_FORM_LINK)
    for n in range(len(input_data["links"])):
        address = input_data["addresses"][n]
        price = input_data["prices"][n]
        link = input_data["links"][n]
        time.sleep(2)
        addr_input = driver.find_elements(By.CLASS_NAME, "whsOnd")[0]
        price_input = driver.find_elements(By.CLASS_NAME, "whsOnd")[1]
        link_input = driver.find_elements(By.CLASS_NAME, "whsOnd")[2]
        addr_input.send_keys(address)
        price_input.send_keys(price)
        link_input.send_keys(link)
        submit_button = driver.find_element(By.CLASS_NAME, "l4V7wb")
        submit_button.click()
        time.sleep(2)
        submit_another_button = driver.find_element(By.CSS_SELECTOR, ".c2gzEf a")
        submit_another_button.click()


fill_in_form(get_apt_listings())
