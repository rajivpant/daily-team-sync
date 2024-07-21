from .messages import generate_daily_message, generate_follow_up_message
from .slack_client import post_to_slack, post_thread_message
from .config import TEAM_MEMBERS
from .slack_client import USER_IDS
print("Fetched User IDs:", USER_IDS)

def main():
    
    # Generate and post the daily message
    daily_message = generate_daily_message()
    daily_message_ts = post_to_slack(daily_message)
    
    # Generate and post follow-up messages for each team member in the thread
    if daily_message_ts:
        for member in TEAM_MEMBERS:
            follow_up_message = generate_follow_up_message(member)
            post_thread_message(daily_message_ts, follow_up_message)

if __name__ == "__main__":
    main()
