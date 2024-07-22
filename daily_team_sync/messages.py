from openai import OpenAI
import random
from daily_team_sync.config import OPENAI_API_KEY, FALLBACK_MESSAGES, MODEL_NAME, TEMPERATURE, DAILY_MESSAGE_PROMPT, FOLLOW_UP_MESSAGE_PROMPT
from daily_team_sync.slack_client import USER_IDS

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_daily_message():
    try:
        response = client.chat.completions.create(model=MODEL_NAME,
        messages=[
            {"role": "system", "content": DAILY_MESSAGE_PROMPT['system']},
            {"role": "user", "content": DAILY_MESSAGE_PROMPT['user']}
        ],
        max_tokens=150,
        temperature=TEMPERATURE)
        message = response.choices[0].message.content.strip()
        return message
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return random.choice(FALLBACK_MESSAGES)

def generate_follow_up_message(team_member):
    try:
        user_id = USER_IDS.get(team_member)
        if not user_id:
            print(f"Could not find User ID for {team_member}")
            return None

        response = client.chat.completions.create(model=MODEL_NAME,
        messages=[
            {"role": "system", "content": FOLLOW_UP_MESSAGE_PROMPT['system']},
            {"role": "user", "content": FOLLOW_UP_MESSAGE_PROMPT['user']}
        ],
        max_tokens=100,
        temperature=TEMPERATURE)
        message = response.choices[0].message.content.strip()
        formatted_message = f"<@{user_id}> {message}"
        return formatted_message
    except Exception as e:
        print(f"OpenAI API error: {e}")
        if user_id:
            return f"<@{user_id}> Just a reminder to post your progress and plans for today."
        else:
            return f"{team_member}, just a reminder to post your progress and plans for today."