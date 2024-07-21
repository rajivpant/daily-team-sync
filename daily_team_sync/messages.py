from openai import OpenAI
import random
from daily_team_sync.config import OPENAI_API_KEY, FALLBACK_MESSAGES, MODEL_NAME, TEMPERATURE
from daily_team_sync.slack_client import USER_IDS

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_daily_message():
    try:
        prompt = "Generate a daily standup message asking for team members' progress, tasks, and hurdles. Include a motivational quote or relevant and tasteful joke. Do not write the robotic greeting 'I hope this message finds you well' or one of its variants."
        response = client.chat.completions.create(model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a project manager who deeply understands, respects, and admires software engineers, designers, and other individual contributors. You have a sense of humor that is appropriate for workplaces."},
            {"role": "user", "content": prompt}
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
        # Get the User ID for the team member
        user_id = USER_IDS.get(team_member)
        if not user_id:
            print(f"Could not find User ID for {team_member}")
            return None

        prompt = f"Generate a friendly follow-up message reminding a team member to share their daily update. Use 'you' instead of their name or username in the message. Do not write the robotic greeting 'I hope this message finds you well' or one of its variants."
        response = client.chat.completions.create(model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a project manager who deeply understands, respects, and admires software engineers, designers, and other individual contributors. You have a sense of humor that is appropriate for workplaces."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=TEMPERATURE)
        message = response.choices[0].message.content.strip()
        # Format the message with proper Slack mention syntax using User ID
        formatted_message = f"<@{user_id}> {message}"
        return formatted_message
    except Exception as e:
        print(f"OpenAI API error: {e}")
        if user_id:
            return f"<@{user_id}> Just a reminder to post your progress and plans for today."
        else:
            return f"{team_member}, just a reminder to post your progress and plans for today."