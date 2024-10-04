import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Function to simulate typing with a delay
def type_with_delay(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3)) 
# Set up Chrome options for incognito mode and disable GPU usage
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-gpu")  # Disables GPU acceleration
chrome_options.add_argument("--no-sandbox")    # Recommended for running Selenium in environments where it might face permissions issues


# Keep the browser open for a while
input("Press Enter to close the browser...")

# Close the browser
driver.quit()
