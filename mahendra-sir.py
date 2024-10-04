from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Navigate to the Gmail login page
driver.get("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

# Wait for the email input field to load
try:
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
except TimeoutException:
    print("Timed out waiting for email input field to load")
    driver.quit()

# Enter the email address
email_input.send_keys("your_email@gmail.com")

# Click the next button
next_button = driver.find_element(By.ID, "identifierNext")
next_button.click()

# Wait for the password input field to load
try:
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
except TimeoutException:
    print("Timed out waiting for password input field to load")
    driver.quit()

# Enter the password
password_input.send_keys("your_password")

# Click the next button
next_button = driver.find_element(By.ID, "passwordNext")
next_button.click()

# Wait for the login to complete
time.sleep(5)

# Check if the login was successful
if driver.title == "Inbox - your_email@gmail.com":
    print("Login successful!")
else:
    print("Login failed!")

# Close the browser
driver.quit()