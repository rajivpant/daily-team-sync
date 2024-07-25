import random
import logging
from litellm import completion
import langcodes
from daily_team_sync.config import (
    FALLBACK_MESSAGES, ENGINE_NAME, MODEL_NAME, TEMPERATURE,
    DAILY_MESSAGE_PROMPT, FOLLOW_UP_MESSAGE_PROMPT,
    MAX_TOKENS_DAILY, MAX_TOKENS_FOLLOW_UP, SUPPORTS_SYSTEM_ROLE,
    config, SKIP_SLACK_POSTING
)
from daily_team_sync.slack_client import USER_IDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_message(prompt, max_tokens, language=None):
    try:
        if SUPPORTS_SYSTEM_ROLE:
            messages = [
                {"role": "system", "content": prompt['system']},
                {"role": "user", "content": prompt['user']}
            ]
        else:
            messages = [
                {"role": "user", "content": prompt['system'] + "\n" + prompt['user']}
            ]

        if language:
            lang_name = langcodes.Language.get(language).display_name()
            messages.append({"role": "user", "content": f"Please generate the response in {lang_name}."})

        logger.info(f"Generating message using {ENGINE_NAME} - {MODEL_NAME}")
        llm_response = completion(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            temperature=TEMPERATURE
        )
        response = llm_response.get('choices', [{}])[0].get('message', {}).get('content')
        return response.strip() if response else None
    except Exception as e:
        logger.error(f"{ENGINE_NAME} API error: {e}")
        return random.choice(FALLBACK_MESSAGES)

def generate_daily_message():
    return generate_message(DAILY_MESSAGE_PROMPT, MAX_TOKENS_DAILY)

def get_team_member_languages(team_member_name):
    for member in config['team_members']:
        if member['name'] == team_member_name:
            return member.get('languages', ['en'])
    return ['en']  # Default to English if not specified

def generate_follow_up_message(team_member_name):
    user_id = USER_IDS.get(team_member_name)
    if not user_id and not SKIP_SLACK_POSTING:
        logger.warning(f"Could not find User ID for {team_member_name}")
        return None

    languages = get_team_member_languages(team_member_name)
    selected_language = random.choice(languages)

    persona = random.choice(config['follow_up_personas'])
    theme = random.choice(config['follow_up_themes'])

    modified_prompt = FOLLOW_UP_MESSAGE_PROMPT.copy()
    modified_prompt['system'] += f" Adopt the persona of a {persona['name']}: {persona['description']}"
    modified_prompt['user'] += f" Focus on the theme of {theme}. Remember, do not use any greeting, name, or @mention - start the message directly."

    message = generate_message(modified_prompt, MAX_TOKENS_FOLLOW_UP, language=selected_language)
    
    if SKIP_SLACK_POSTING:
        return f"Follow-up for {team_member_name}: {message}" if message else None
    else:
        return f"<@{user_id}> {message}" if message else None
