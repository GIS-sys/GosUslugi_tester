import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

GECKODRIVER_PATH="/usr/bin/geckodriver"

def waitGetElement(driver, args):
    return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(args))


# Create a Firefox instance with options
options = Options()
options.headless = False  # Set to True if you want to run in headless mode
driver = webdriver.Firefox(executable_path=GECKODRIVER_PATH, options=options)

driver.get(f"http://localhost:8080")
allElements = waitGetElement(driver, (By.XPATH, "//div//span[contains(@class, 'a')][contains(@class, 'b')]"))
for x in allElements:
    print(x.tag_name, x.text, x.get_attribute("innerHTML"))

driver.close()

