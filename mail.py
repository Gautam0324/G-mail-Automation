import undetected_chromedriver as uc
import time
import random
from selenium.webdriver.common.by import By

# Function to add random sleep
def random_sleep():
    time.sleep(random.uniform(1, 3))

# Initialize undetected Chrome
options = uc.ChromeOptions()
# Set a custom user-agent
options.add_argument('user-agent=Your-Custom-User-Agent')

# Start the browser with options
driver = uc.Chrome(options=options)

# Randomize window size
width = random.randint(1024, 1920)
height = random.randint(768, 1080)
driver.set_window_size(width, height)

# Open Gmail login page
driver.get('https://accounts.google.com/')

# Wait for the page to load
random_sleep()

# Enter the email address
email_input = driver.find_element(By.ID, 'identifierId')
email_input.send_keys('taniksaer@gmail.com')  # Replace with your email
random_sleep()

# Click on the Next button
next_button = driver.find_element(By.ID, 'identifierNext')
next_button.click()
random_sleep()

# Wait for the password field to load
time.sleep(3)  # You can adjust this if needed

# Enter the password
password_input = driver.find_element(By.NAME, 'password')
password_input.send_keys('Lc&575135')  # Replace with your password
random_sleep()

# Click on the Next button
next_button = driver.find_element(By.ID, 'passwordNext')
next_button.click()
random_sleep()

# Wait for the Gmail interface to load
time.sleep(10)  # You may adjust this based on your connection speed

# Click on the Compose button (ensure the selector matches the element)
compose_button = driver.find_element(By.CSS_SELECTOR, 'div[gh="cm"]')
compose_button.click()

# Optionally, wait and close the browser
random_sleep()
driver.quit()
