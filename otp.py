import os
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

# Create a Twilio client object
client = Client(account_sid, auth_token)

# Generate a random OTP (6 digits in this example)
otp = str(random.randint(100000, 999999))

# Replace with the phone number you want to send the OTP to
phone_number = "+1234567890"

# Create a message with the OTP
message = client.messages.create(
    body=f"Your OTP is: {otp}",
    from_="+917014236409",  # Replace with your Twilio phone number
    to=phone_number
)

print(f"OTP sent to {phone_number}: {otp}")