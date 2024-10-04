import time
import random 
import pyautogui  
from botasaurus.browser import browser, Driver, Wait
from selenium.webdriver.common.keys import Keys
from playwright.sync_api import sync_playwright



# Define the Google credentials
GOOGLE_EMAIL = "saatheasty@gmail.com"
GOOGLE_PASSWORD = "Asoei@10202"

#define Sender EMAIL 
SENDER_EMAIL = "saatheasty@gmail.com"

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

    #check login 
    try:
        compose_button = driver.get_element_with_exact_text("Compose", wait=Wait.SHORT)
        if compose_button:
            print("User is already logged in. Skipping login process and starting email composition.")
            start_composing_emails(driver)  # If logged in, start composing
            return
    except Exception:
        print("User is not logged in. Proceeding with login process...")

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

# Function to compose and send emails
def start_composing_emails(driver: Driver):
    for recipient in SENDER_EMAIL:
        time.sleep(2)  # Ensure that the inbox is fully loaded
        
        # Step 7: Click the "Compose" button
        try:
            compose_button = driver.get_element_with_exact_text("Compose", wait=Wait.LONG)
            compose_button.click()
        except Exception as e:
            print(f"Compose button not found for {recipient}: {str(e)}")
            continue  # Skip to the next recipient if the compose button is not found

        # Step 8: Add recipient email
        sender_input = driver.wait_for_element("input[id='message-to-field']", wait=Wait.LONG)
        type_with_delay(sender_input, recipient)

        # Step 9: Add the subject
        subject_input = driver.wait_for_element("input[data-test-id='compose-subject']", wait=Wait.LONG)
        type_with_delay(subject_input, SUBJECT)
        pyautogui.hotkey('tab')
        
        # Open a new tab using the Ctrl + T shortcut
        pyautogui.hotkey('ctrl', 't')
    
        # Navigate to the specific link
        pyautogui.typewrite('https://m.phx.co.in/a/mailer.html')
        pyautogui.press('enter')
        time.sleep(5)
        # Select all content on the page using Ctrl + A
        pyautogui.hotkey('ctrl', 'a')

        # Copy the selected content using Ctrl + C
        pyautogui.hotkey('ctrl', 'c')
        pyautogui.hotkey('ctrl', 'w')
        
        time.sleep(2)
        # Switch back to the original tab
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        time.sleep(2)
        pyautogui.hotkey('tab')
        time.sleep(2)
        # Step 10: Add the body
        # body_input = driver.wait_for_element("div[role='textbox']", wait=Wait.LONG)
        # type_with_delay(body_input, BODY)
        pyautogui.hotkey('ctrl',  'v')
        time.sleep(3)
        # Step 11: Click the "Send" button
        try:
                send_button = driver.get_element_with_exact_text("Send", wait=Wait.LONG)
                send_button.click()
                print(f"Email successfully sent to {recipient}.")
        except Exception as e:
                print(f"Send button not found for {recipient}: {str(e)}")

        # Optional: Delay between sending emails
        time.sleep(2)

# Execute the login task
google_login_task(data=None)