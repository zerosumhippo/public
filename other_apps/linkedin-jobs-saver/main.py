from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

LI_EMAIL = os.environ.get("LI_EMAIL")
LI_PW = os.environ.get("LI_PW")

chrome_driver_path = "C:/Users/breim/Development/chromedriver.exe"
service = Service(f"r{chrome_driver_path}")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3564001002&f_AL=true&f_WT=2&keywords=data%20engineer"
           "&refresh=true")

sign_in_button = driver.find_element(By.CSS_SELECTOR, ".nav__button-secondary")
time.sleep(2)
sign_in_button.click()
time.sleep(2)

email_entry = driver.find_element(By.ID, "username")
email_entry.send_keys(LI_EMAIL)
pw_entry = driver.find_element(By.ID, "password")
pw_entry.send_keys(LI_PW)
sign_in = driver.find_element(By.CSS_SELECTOR, ".btn__primary--large")
sign_in.click()
time.sleep(5)

save_job = driver.find_element(By.CSS_SELECTOR, ".jobs-save-button")
save_job.click()
follow_company = driver.find_element(By.CSS_SELECTOR, ".follow .artdeco-button__icon")
follow_company.click()
