from config import GECKODRIVER_PATH

import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

# Create a Firefox instance with options
options = Options()
options.headless = False  # Set to True if you want to run in headless mode
driver = webdriver.Firefox(executable_path=GECKODRIVER_PATH, options=options)

# Go to the specific website
driver.get("https://medmobil.ru")

# Wait for the page to load and find all buttons with class "button-widget-open"
buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "button-widget-open")))

# Click a random button
random_button = random.choice(buttons)
random_button.click()

# Wait for 2 seconds (to observe the result) and then close the browser
time.sleep(2)
driver.quit()

