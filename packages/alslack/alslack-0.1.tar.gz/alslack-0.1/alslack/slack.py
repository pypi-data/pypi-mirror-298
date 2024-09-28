# import json
import requests
# import os

class Slack:
    def __init__(self, bot_token=None):
        self.bot_token = bot_token # Slack bot token used to authenticate with the Slack API
        self.slack_url = "https://slack.com/api/chat.postMessage" # URL of the slackAPI

    def send_text_response(self, channel_id, response_text):
        if not self.bot_token:
            print("Error: Slack bot token is not set.")
            return {"ok": False, "error": "Slack bot token not set"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.bot_token}"
        }
        data = {
            "channel": channel_id,
            "text": response_text,
            "link_names": True
        }
        
        try:
            response = requests.post(self.slack_url, headers=headers, json=data)
            response_data = response.json()
            if not response_data.get("ok"):
                print(f"Error sending message: {response_data.get('error')}")
            else:
                print(f"Message sent to Slack: {response_data}")
            return response_data
        except Exception as e:
            print('Error sending message to Slack:', e)
            return {"ok": False, "error": str(e)}

