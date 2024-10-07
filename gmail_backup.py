import time
import random 
import pyautogui  
from botasaurus.browser import browser, Driver, Wait 
from selenium.webdriver.common.keys import Keys
from playwright.sync_api import sync_playwright
import subprocess
import requests



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

# Function to run ADB commands
def run_adb_command(command):

    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error running ADB command: {e.stderr.decode('utf-8')}")
        return None


def get_current_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        return response.json().get('ip')
    except requests.RequestException as e:
        print(f"Error fetching current IP: {e}")
        return None
    
# Function to change the IP address by toggling flight mode
def change_ip():
    try:
        print('Enabling flight mode...')
        run_adb_command('adb shell cmd connectivity airplane-mode enable')
        print('Waiting for 10 seconds...')
        time.sleep(10)
        
        print('Disabling flight mode...')
        run_adb_command('adb shell cmd connectivity airplane-mode disable')
        print('Waiting for 20 seconds...')
        time.sleep(20)  # Increase this wait time to allow the network to stabilize
        
        print('Waiting for IP to change...')
        time.sleep(10)

        
        new_ip = get_current_ip()
        
        if new_ip:
            print(f"New IP: {new_ip}")
        else:
            print("New IP not found!")

        return new_ip
    except Exception as error:
        print('Error during IP change:', error)
        return None

def is_ip_used(ip, filename='yahoo.txt'):
    
    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            used_ips = file.read().splitlines()
            
            # Loop through each line in the file
            for entry in used_ips:
                # Split the IP and the date (if present) and compare only the IP part
                stored_ip = entry.split(' - ')[0].strip()  # Extract the IP part and remove extra spaces
                if stored_ip == ip:
                    return True  # IP is already used
            return False  # IP not found in the file
    except FileNotFoundError:
        # If the file doesn't exist, consider that no IP has been used yet
        return False
    

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
    new_ip = change_ip()
    if new_ip and not is_ip_used(new_ip):
     time.sleep(2)  # Ensure that the inbox is fully loaded
            

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
    pyautogui.hotkey('ctrl',  'v')

    # To click the  send button
    
    send_button = driver.get_element_with_exact_text("Send", wait=Wait.LONG)
    send_button.click()

    time.sleep(1)
    Message_body = driver.wait_for_element("input[role='textbox']", wait=Wait.LONG)
    # type_with_delay(Message_body, BODY)


# Execute the login task
google_login_task(data=None)