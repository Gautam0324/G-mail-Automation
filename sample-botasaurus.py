import pandas as pd
import json
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import os
from shutil import copyfile
from botasaurus_driver import Driver
from botasaurus.browser import Wait

# A list of User-Agents to randomize
user_agents = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
# Add more user-agents...
]

# # CSV Paths
# input_csv = './cvrt.csv'
# processed_csv = './processed.csv'
# backup_csv = './cvrt_backup.csv'

# Backup the original CSV before any processing
if not os.path.exists(backup_csv):
copyfile(input_csv, backup_csv)

# Read CSV data
df = pd.read_csv(input_csv, dtype={'checker': 'string', 'Email': 'string', "laptop": "string"})
if os.path.exists(processed_csv):
processed_df = pd.read_csv(processed_csv)
else:
processed_df = pd.DataFrame()

# Lock for thread-safe CSV updates
csv_lock = Lock()

results = [] # To store results of each row processing

# Function to get the current IP address using a proxy
def get_current_ip_with_proxy(proxy_url):
import requests
proxies = {"http": proxy_url, "https": proxy_url}
try:
response = requests.get('https://api.ipify.org?format=json', proxies=proxies)
# response = requests.get('https://api.ipify.org?format=json')
response.raise_for_status()
return response.json().get('ip')
except requests.RequestException as e:
print(f"Error fetching current IP with proxy: {e}")
return None

# Function to check if the IP is already used
def is_ip_used(ip, filename='cvrt.txt'):
try:
with open(filename, 'r') as file:
used_ips = file.read().splitlines()
return any(stored_ip.split(' - ')[0].strip() == ip for stored_ip in used_ips)
except FileNotFoundError:
return False

# Function to save the IP address to a file
def save_ip(ip, gmail, phone, filename='./cvrt.txt'):
current_date = datetime.now().strftime('%Y-%m-%d')
with open(filename, 'a') as file:
file.write(f"{ip} - {current_date} - {gmail} - {phone}\n")

# Function to simulate human typing
def type_like_human(element, text):
for char in text:
element.type(char)
time.sleep(random.uniform(0.1, 0.3)) # Random delay between key presses

# Function to check if the row is already processed
def is_row_processed(row):
email = row.get('Email', None) # Use .get() to avoid KeyError
if not email:
print(f"Warning: Missing 'Email' column for row {row}")
return True # Treat missing 'Email' column as processed to avoid reprocessing
return not processed_df[processed_df['Email'] == email].empty

# Scraper function that processes each row of data
def process_row(index, row):
try:
print(f"Processing row {index}: {row.to_dict()}")

# Debugging: Print all column names and check for potential issues
print(f"Available columns in row {index}: {list(row.index)}")

# Ensure the column exists and handle missing 'Email' cases
email = row.get('Email', None) # Use .get() to avoid KeyError
if not email:
print(f"Warning: Missing 'Email' column for row {index}")
return # Skip this row if 'Email' is missing

# Continue processing the row
if pd.isna(row['checker']) or row['checker'].upper() == "FALSE":
print(f"Checker is False or NA for row {index}. Proceeding...")

# Setup the proxy
# proxy_url = f"http://{row['username']}:{row['password']}@{row['host']}:{row['port']}"
proxy_url = f"192.168.71.10:8080"
print(f"Using proxy: {proxy_url}")

# Get current IP through the proxy
new_ip = get_current_ip_with_proxy(proxy_url)
if new_ip and not is_ip_used(new_ip):
print(f"New IP for row {index}: {new_ip}")

# Select a random User-Agent
user_agent = random.choice(user_agents)
print(f"Using User-Agent for row {index}: {user_agent}")

# Initialize Botasaurus driver with proxy and random User-Agent
driver = Driver(proxy=proxy_url, user_agent=user_agent)
# driver = Driver(user_agent=user_agent, block_images=True)
try:
# # Access the website and wait for a key element to ensure the page has loaded
driver.get("https://gbplaces.com/little")
driver.block_urls(["*://optimizationguide-pa.googleapis.com/*"])
driver.wait_for_element("input#mainform_F_3_FIRSTNAME", wait=Wait.LONG)

# Simulate typing for the first name
element3 = driver.select("input#mainform_F_3_FIRSTNAME")
driver.type("input#mainform_F_3_FIRSTNAME", "")
type_like_human(element3, row['Name'])
time.sleep(random.uniform(3, 4))

# Simulate typing for the email (Email is now guaranteed to exist)
element5 = driver.select("input#mainform_F_1_EMAIL")
driver.type("input#mainform_F_1_EMAIL", "")
type_like_human(element5, email)
time.sleep(random.uniform(3, 4))

# Simulate typing for the mobile number
element7 = driver.select("input#mainform_F_12_PHONE1")
driver.type("input#mainform_F_12_PHONE1", "")
type_like_human(element7, str(row['Mobile']))
time.sleep(random.uniform(3, 4))

# Click consent checkbox
element9 = driver.select("input#mainform_F_3499_CONSENT_TERMS_AGREE")
element9.click()
time.sleep(random.uniform(15, 20))

# Click submit button
# driver.click("input.btn.btn-danger")
element11 = driver.select("input.btn-danger")
element11.click()
time.sleep(random.uniform(15, 20))

# Lock before modifying the DataFrame
with csv_lock:
processed_row = df.loc[[index]].copy() # Get the processed row
processed_row.to_csv(processed_csv, mode='a', header=False, index=False) # Append to processed.csv
df.drop(index, inplace=True) # Drop the row from the original DataFrame
df.to_csv(input_csv, index=False) # Save the remaining rows back to the original CSV

print(f"Row {index} processed successfully")
save_ip(new_ip, gmail=email, phone=row['Mobile'])

except Exception as e:
print(f"Error processing row {index}: {e}")

finally:
print("Pausing for manual inspection, press Enter to continue...")
driver.prompt() # Pauses the browser until user input
driver.close() # Close the Botasaurus browser session properly
else:
print(f"IP is already used or could not fetch IP for row {index}. Skipping.")
with csv_lock:
df.at[index, 'checker'] = "false"
df.at[index, 'laptop'] = "PC429"
else:
print(f"Checker is already true for row {index}. Skipping.")

except Exception as e:
print(f"Exception occurred for row {index}: {e}")

# Function to run scrapers in parallel
def run_in_parallel():
# Define the maximum number of parallel threads (adjust based on system capacity)
max_threads = 1

with ThreadPoolExecutor(max_workers=max_threads) as executor:
futures = {executor.submit(process_row, index, row): index for index, row in df.iterrows()}
for future in as_completed(futures):
index = futures[future]
try:
future.result()
except Exception as exc:
print(f"Row {index} generated an exception: {exc}")

if __name__ == "__main__":
print("Starting scraping process...")
run_in_parallel() # Start the parallel scraping process