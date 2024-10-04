import time
import random 
import pyautogui  
from botasaurus.browser import browser, Driver, Wait
from selenium.webdriver.common.keys import Keys
from playwright.sync_api import sync_playwright



# Define the Google credentials
# Replace with mail you want to Login 
GOOGLE_EMAIL = "XYZ@gmail.com"
#Replace with your Password 
GOOGLE_PASSWORD = "XYZXX"

#define Sender EMAIL 

# Replace with mail you want to Send 

SENDER_EMAIL = "XYZ@gmail.com"

# Subject 
SUBJECT = "Gmail Automation Done "

#Message body
BODY =  ""


 # Function to simulate typing with a delay
def type_with_delay(element, text):
    for char in text:
        element.type(char)
        time.sleep(random.uniform(0.001, 0.002))  # Random delay between keystrokes

@browser()

# @browser(tiny_profile=True, 
#     profile=GOOGLE_EMAIL)
def google_login_task(driver: Driver, data):
    # Step 1: Navigate to Google Sign-In page
    driver.get("https://mail.google.com/mail/u/0/#inbox")

    # Step 2: Enter the email
    email_input = driver.wait_for_element("input[type='email']", wait=Wait.LONG)
    type_with_delay(email_input, GOOGLE_EMAIL)
    driver.select("#identifierNext").click()

    # Step 3: Wait for the password field and enter the password
     # Short sleep for password input to appear
    time.sleep(2)
    password_input = driver.wait_for_element("input[type='password']", wait=Wait.LONG)
    type_with_delay(password_input, GOOGLE_PASSWORD)
    driver.select("#passwordNext").click()

    # Step 4: Wait for login to complete (adjust timing as needed)
    # time.sleep(10)

    # Step 5: Handle any "Not now" or post-login confirmation dialogs
    try:
        not_now_button = driver.get_element_with_exact_text("Not now", wait=Wait.LONG)
        not_now_button.click()
    except Exception as e:
        print("Not now button not found, proceeding anyway...")

    # Step 6: To click The Compose Button 
    time.sleep(0.1)  # Ensure that the inbox is fully loaded

    try:
        compose_button = driver.get_element_with_exact_text("Compose", wait=Wait.LONG)
        compose_button.click()
    except Exception as e:
    
    
    # To click to type sender mail id 
        time.sleep(3)
        Recipients_button = driver.get_element_with_exact_text("Recipients", wait=Wait.LONG)
        Recipients_button.click()

    # To sender mail id 
    sender_input = driver.wait_for_element("input[type='text']", wait=Wait.LONG)
    type_with_delay(sender_input, SENDER_EMAIL)
    # driver.select("#:rj").click()

    pyautogui.press('tab')
    # To click to type subject
    subject_input = driver.wait_for_element("input[name='subjectbox']", wait=Wait.LONG)
    type_with_delay(subject_input, SUBJECT)

    # Open another tab 
    # Open a new tab using the Ctrl + T shortcut
    pyautogui.hotkey('ctrl', 't')
    
    # Navigate to the specific link
    pyautogui.typewrite('https://m.phx.co.in/a/mailer.html')
    pyautogui.press('enter')
    
    # Wait for the page to load
    time.sleep(2)

    # Select all content on the page using Ctrl + A
    pyautogui.hotkey('ctrl', 'a')

    # Copy the selected content using Ctrl + C
    pyautogui.hotkey('ctrl', 'c')

    # Switch back to the original tab
    pyautogui.hotkey('ctrl', 'shift', 'tab')
    pyautogui.press('tab')

    # To click to type body
    body_input = driver.wait_for_element("div[role='textbox']", wait=Wait.LONG)
    # Paste the copied content using Ctrl + V
    pyautogui.hotkey('ctrl', 'v')

    # To click the  send button
    
    send_button = driver.get_element_with_exact_text("Send", wait=Wait.LONG)
    send_button.click()

    time.sleep(1)
    Message_body = driver.wait_for_element("input[role='textbox']", wait=Wait.LONG)
    # type_with_delay(Message_body, BODY)


# Execute the login task
google_login_task(data=None)