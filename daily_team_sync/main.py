import os
import sys
import logging
import socket

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from daily_team_sync.messages import generate_daily_message, generate_follow_up_message
from daily_team_sync.slack_client import post_to_slack, post_thread_message, USER_IDS
from daily_team_sync.config import config, ENGINE_NAME, engine_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dns():
    try:
        socket.gethostbyname('api.slack.com')
        return True
    except socket.gaierror:
        logger.error("DNS resolution failed. Please check your internet connection and DNS settings.")
        return False

def check_api_key():
    try:
        api_key_name = next(engine['api_key_name'] for engine in engine_config['engines'] if engine['name'] == ENGINE_NAME)
        api_key = os.getenv(api_key_name)
        if not api_key:
            logger.error(f"API key for {ENGINE_NAME} is not set. Please check your .env file.")
            return False
        return True
    except StopIteration:
        logger.error(f"No configuration found for engine {ENGINE_NAME}")
        return False

def main():
    if not check_api_key():
        return

    try:
        # Generate and post the daily message
        daily_message = generate_daily_message()
        if daily_message:
            daily_message_ts = post_to_slack(daily_message)
            
            # Generate and post follow-up messages for each team member
            if daily_message_ts:
                for member in config['team_members']:
                    follow_up_message = generate_follow_up_message(member['name'])
                    if follow_up_message:
                        post_thread_message(daily_message_ts, follow_up_message)
            else:
                logger.error("Failed to post daily message to Slack.")
        else:
            logger.error("Failed to generate daily message.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if not check_dns():
        sys.exit(1)
    if not USER_IDS:
        logger.warning("No user IDs available. Mentions in messages may not work correctly.")
    main()
