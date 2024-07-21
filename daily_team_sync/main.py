import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from daily_team_sync.messages import generate_daily_message, generate_follow_up_message
from daily_team_sync.slack_client import post_to_slack, post_thread_message
from daily_team_sync.config import TEAM_MEMBERS

def main():
    # Generate and post the daily message
    daily_message = generate_daily_message()
    daily_message_ts = post_to_slack(daily_message)
    
    # Generate and post follow-up messages for each team member
    if daily_message_ts:
        for member in TEAM_MEMBERS:
            follow_up_message = generate_follow_up_message(member)
            if follow_up_message:
                post_thread_message(daily_message_ts, follow_up_message)

if __name__ == "__main__":
    main()