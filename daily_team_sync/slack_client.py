from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .config import SLACK_BOT_TOKEN, SLACK_CHANNEL, TEAM_MEMBERS

client = WebClient(token=SLACK_BOT_TOKEN)

def fetch_user_ids():
    user_ids = {}
    try:
        response = client.users_list()
        for member in response["members"]:
            # Check against display name, real name, and username
            if member["profile"].get("display_name") in TEAM_MEMBERS or \
               member["profile"].get("real_name") in TEAM_MEMBERS or \
               member.get("name") in TEAM_MEMBERS:
                user_ids[member["profile"].get("display_name") or member["profile"].get("real_name") or member.get("name")] = member["id"]
    except SlackApiError as e:
        print(f"Error fetching user list: {e}")
    return user_ids

USER_IDS = fetch_user_ids()

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