import os 
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Hello, from Twilio and Python!",
    to="+639692956701",
    from_='+19706388875',
)

print(f"message: {message.body}")
print(f"sent from: {message.from_}")
print(f"sent to: {message.to}")