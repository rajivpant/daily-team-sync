import random
from litellm import completion
from daily_team_sync.config import (
    FALLBACK_MESSAGES, ENGINE_NAME, MODEL_NAME, TEMPERATURE,
    DAILY_MESSAGE_PROMPT, FOLLOW_UP_MESSAGE_PROMPT,
    MAX_TOKENS_DAILY, MAX_TOKENS_FOLLOW_UP, SUPPORTS_SYSTEM_ROLE,
    config
)
from daily_team_sync.slack_client import USER_IDS

def generate_message(prompt, max_tokens):
    try:
        if SUPPORTS_SYSTEM_ROLE:
            messages = [
                {"role": "system", "content": prompt['system']},
                {"role": "user", "content": prompt['user']}
            ]
        else:
            messages = [
                {"role": "user", "content": prompt['system']},
                {"role": "user", "content": prompt['user']}
            ]

        llm_response = completion(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            temperature=TEMPERATURE
        )
        response = llm_response.get('choices', [{}])[0].get('message', {}).get('content')
        return response.strip() if response else None
    except Exception as e:
        print(f"{ENGINE_NAME} API error: {e}")
        return random.choice(FALLBACK_MESSAGES)

def generate_daily_message():
    return generate_message(DAILY_MESSAGE_PROMPT, MAX_TOKENS_DAILY)

def generate_follow_up_message(team_member):
    user_id = USER_IDS.get(team_member)
    if not user_id:
        print(f"Could not find User ID for {team_member}")
        return None

    # Select a random persona and theme
    persona = random.choice(config['follow_up_personas'])
    theme = random.choice(config['follow_up_themes'])

    # Modify the follow-up prompt with the selected persona and theme
    modified_prompt = FOLLOW_UP_MESSAGE_PROMPT.copy()
    modified_prompt['system'] += f" Adopt the persona of a {persona['name']}: {persona['description']}"
    modified_prompt['user'] += f" Focus on the theme of {theme}."

    message = generate_message(modified_prompt, MAX_TOKENS_FOLLOW_UP)
    return f"<@{user_id}> {message}" if message else None
