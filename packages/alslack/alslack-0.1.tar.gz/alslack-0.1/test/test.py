# This test script is ran locally and is used to import the Slack class as well as the CostAlerterClient class. 
# It processes the sqs payload and sends the costalerter message to the slack channel.

import json
#import os
import sys
#from modules.costalerter_client import CostAlerterClient  
#from alslack.slack import Slack  
from alsacommonutils import al_common_aws_utils as awsutils 

# Added the absolute path of slack.py and costalerter_client.py on the local machine to the Python path
sys.path.append('/home/georgerb/repos/al-aws-notification-modules/code/channels/slack/alslack')
from slack import Slack

sys.path.append('/home/georgerb/repos/al-aws-notification-modules/code/connectors/costalerter/modules')
from costalerter_client import CostAlerterClient

class TestContext:
    def __init__(self):
        self.aws_request_id = "test-request-id"

if __name__ == "__main__":

    # SQS event payload
    sqs_event = {
        "Records": [
            {
            "messageId": "05d988d2-f78b-4f8d-8022-f5b266a20a3f",
            "receiptHandle": "AQEBw5y5TX1JVLhUKFqDIZUmnJyWRfPdd7E6vKjcHpdecAN1DQ9dT2kF+U7Drb3ig4nrV1emwhQj8OKLgJcW4E9abBLo+804cLRhZ9tsvv/j0a2wP9Fq44/7H1JlOdRKZSUcOlLdGR1UmZlEg8zULUuiMP++bbio9tpCjEU5OcputzwE4vRncf/JLVn2D6qqthwUQBsmZY/619MjYMuhgdqG6gD2MN6ouvkkj6mGEueO4kqtbJqZGebt/m65vWM2aEz0kHMM98of7efwBTkNcw3gkXY3dvFz4yODcNNKXXaoo6uFA5SqF/2JBy9LDeqfavsHipwb4FOzG9XyeZPDAE3wY+YCSNNY5zVs/sYmEGNsXtNXWLanCjA+fxDu42WwnT9Of9C6686/uumGXtI3k9Voxw==",
            "body": {
                "account_id": "978926089958",
                "account_name": "TEST-ACCOUNT",
                "budget_amount": 5.0,
                "total_amount": "6.20",
                "resources": [
                {
                    "Account": "978926089958",
                    "Name": "Amazon QuickSight",
                    "Amount": 3.4,
                    "Unit": "USD"
                },
                {
                    "Account": "978926089958",
                    "Name": "EC2 - Other",
                    "Amount": 1.06,
                    "Unit": "USD"
                }
                ],
                "TimePeriod": {
                "Start": "2024-06-24",
                "End": "2024-06-25"
                },
                "notification_platform": [
                "email",
                "whatsapp",
                "slack",
                "teams"
                ],
                "scan_datetime": "2024-06-25 09:22 AM",
                "frequency": "hourly",
                "resources_count_limit": "4",
                "minimum_amount_value": "1",
                "total_resources_count": 21,
                "currency": "$",
                "notification_teams": [
                {
                    "teams_channel": "DevOps-Costs",
                    "teams_name": "AL Budgets"
                }
                ],
                "notification_whatsapp": {
                "template_name": "costalerter",
                "individual": [
                    {
                    "name": "Jay",
                    "address": "27828202809"
                    },
                    {
                    "name": "Francis",
                    "address": "27842658525"
                    }
                ],
                "groups": [
                    {
                    "groupname": "Test Group",
                    "groupid": "120363303926311567@g.us"
                    }
                ]
                },
                "notification_slack": [
                {
                    "slack_channel": "C07DY6QSK6Y"  # Replace with your actual Slack channel ID
                }
                ]
            },
            "attributes": {
                "ApproximateReceiveCount": "1",
                "AWSTraceHeader": "Root=1-66578721-0e3286c97abaf5046d4e4eab;Parent=43e8b97b5ac4be9e;Sampled=0;Lineage=fafde5d7:0",
                "SentTimestamp": "1717012260350",
                "SenderId": "AROAUREG6N2TEPELTPEMP:send_to_sqs",
                "ApproximateFirstReceiveTimestamp": "1717012260358"
            },
            "messageAttributes": {},
            "md5OfBody": "84630f15c3ca120c18a9a443b550fd64",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:eu-west-1:311668141734:my-al-test-sqs-queue",
            "awsRegion": "eu-west-1"
            }
        ]
    }

    # test context (emulates Lambda context)
    context = TestContext()

    # Prepare the message template
    message_template = (
        "AWS Account: {{aws_account_id}}\n"
        "Account Name: {{aws_account_name}}\n"
        "Budget Amount: {{aws_budget_amount}}\n"
        "Total Amount: {{aws_total_amount}}\n"
        "Period: {{start_period}} to {{end_period}}\n"
        "Resources:\n{{resource_list}}"
    )

    # Initialize the CostAlerterClient with the above SQS event
    costalerter_client = CostAlerterClient(sqs_event)
    message = costalerter_client.prepare_messages(message_template)

    # Retrieve Slack bot token from Secrets Manager
    slack_credentials = json.loads(awsutils.get_secret("al/slack-channel/bot-token", "eu-west-1"))
    slackBotToken = slack_credentials["SlackBotToken"]

   # Initialize Slack client. This slack_client will expect the channel_id and message as parameters.
    slack_client = Slack(slackBotToken)  

    # Retrieve the Slack channel ID from the SQS message
    slackChannelID = costalerter_client.get_slack_channel()

    # Send the processed message to Slack
    slack_result = slack_client.send_text_response(slackChannelID, message)

    # Print the result
    print(slack_result)
    print('Message sent to Slack')
