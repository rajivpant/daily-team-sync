import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from daily_team_sync.config import SKIP_SLACK_POSTING, SLACK_BOT_TOKEN, SLACK_CHANNEL, config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = WebClient(token=SLACK_BOT_TOKEN) if not SKIP_SLACK_POSTING else None

def fetch_user_ids():
    if SKIP_SLACK_POSTING:
        return {member['name']: f"USER_ID_{index}" for index, member in enumerate(config['team_members'])}

    user_ids = {}
    try:
        response = client.users_list()
        team_member_names = [member['name'] for member in config['team_members']]
        for member in response["members"]:
            if member["profile"].get("display_name") in team_member_names or \
               member["profile"].get("real_name") in team_member_names or \
               member.get("name") in team_member_names:
                user_ids[member["profile"].get("real_name") or member.get("name")] = member["id"]
    except SlackApiError as e:
        logger.error(f"Error fetching user list: {e}")
    except Exception as e:
        logger.error(f"Unexpected error when fetching user list: {e}")
    return user_ids

USER_IDS = fetch_user_ids()

def post_to_slack(message):
    if SKIP_SLACK_POSTING:
        logger.info(f"SKIP_SLACK_POSTING: Would post to Slack channel {SLACK_CHANNEL}:\n{message}")
        return "skip_slack_posting_timestamp"
    else:
        try:
            response = client.chat_postMessage(
                channel=SLACK_CHANNEL,
                text=message
            )
            return response['ts']
        except SlackApiError as e:
            logger.error(f"Slack API error: {e.response['error']}")
        except Exception as e:
            logger.error(f"Unexpected error when posting to Slack: {e}")
    return None

def post_thread_message(parent_ts, message):
    if SKIP_SLACK_POSTING:
        logger.info(f"SKIP_SLACK_POSTING: Would post thread message to Slack channel {SLACK_CHANNEL}, parent ts {parent_ts}:\n{message}")
    else:
        try:
            response = client.chat_postMessage(
                channel=SLACK_CHANNEL,
                thread_ts=parent_ts,
                text=message
            )
        except SlackApiError as e:
            logger.error(f"Slack API error: {e.response['error']}")
        except Exception as e:
            logger.error(f"Unexpected error when posting thread message: {e}")
