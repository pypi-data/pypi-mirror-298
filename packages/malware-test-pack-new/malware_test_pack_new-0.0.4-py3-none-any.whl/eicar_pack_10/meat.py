import requests
import json

# Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1289453262231306294/2mvDt8pJ2IgFGGTSuPX461D1sioknPfj7P5di4hxmIxD95IZZRWqN4v7K9q13H2NcQXj"

# Message payload
payload = {
    "content": "Hello"
}

# Send the message
response = requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

# Check if the message was sent successfully
if response.status_code == 204:
    print("Message sent successfully!")
else:
    print(f"Failed to send message: {response.status_code}, {response.text}")
