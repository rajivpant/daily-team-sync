from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .config import SLACK_BOT_TOKEN, SLACK_CHANNEL

client = WebClient(token=SLACK_BOT_TOKEN)

def post_to_slack(message):
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=message
        )
        return response['ts']
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")
        return None

def post_thread_message(parent_ts, message):
    try:
        response = client.chat_postMessage(
            channel=SLACK_CHANNEL,
            thread_ts=parent_ts,
            text=message
        )
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")