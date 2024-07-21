from openai import OpenAI

import random
from .config import OPENAI_API_KEY, FALLBACK_MESSAGES, MODEL_NAME, TEMPERATURE

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_daily_message():
    try:
        prompt = "Generate a daily standup message asking for team members' progress, tasks, and hurdles. Include a motivational quote or relevant and tasteful joke. Do not write the robotic greeting 'I hope this message finds you well' or one of its variants."
        response = client.chat.completions.create(model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a project manager who deeply undertands, respects, and admires software engineers, designers, and other individual contributors. You have a sense of humor that is appropriate for workplaces."},
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
        prompt = f"Generate a friendly follow-up message for {team_member} reminding them to share their daily update. Tag them using the @ mention format. Do not write the robotic greeting 'I hope this message finds you well' or one of its variants."
        response = client.chat.completions.create(model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a project manager who deeply undertands, respects, and admires software engineers, designers, and other individual contributors. You have a sense of humor that is appropriate for workplaces."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=TEMPERATURE)
        message = response.choices[0].message.content.strip()
        return message
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return f"Hi {team_member}, just a reminder to post your progress and plans for today."
