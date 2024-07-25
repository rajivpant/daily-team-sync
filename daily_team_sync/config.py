import os
import yaml
from dotenv import load_dotenv
import random
import logging
from litellm import completion
import socket

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the project root directory
project_root = os.path.dirname(current_dir)

# Load environment variables from .env file
load_dotenv(os.path.join(project_root, '.env'))

# Set API keys from environment variables
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

# Load configuration from config.yaml
config_path = os.path.join(project_root, 'config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

# Skip Slack posting setting
SKIP_SLACK_POSTING = config['settings'].get('skip_slack_posting', False)

FALLBACK_MESSAGES = config['fallback_messages']
TEAM_MEMBERS = config['team_members']
SLACK_CHANNELS = config['slack']['channels']
ACTIVE_CHANNEL = config['slack']['active_channel']
SLACK_CHANNEL = SLACK_CHANNELS[ACTIVE_CHANNEL]

# Load prompts
DAILY_MESSAGE_PROMPT = config['prompts']['daily_message']
FOLLOW_UP_MESSAGE_PROMPT = config['prompts']['follow_up_message']

# Load engine settings from engines.yaml
engines_path = os.path.join(project_root, 'engines.yaml')
with open(engines_path, 'r') as file:
    engine_config = yaml.safe_load(file)

def check_internet_connection():
    try:
        # Try to resolve Google's DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        logger.warning("No internet connection detected.")
        return False

def validate_api_key(engine_name, model_name, api_key):
    if not check_internet_connection():
        logger.warning(f"Skipping API key validation for {engine_name} due to no internet connection.")
        return True  # Assume the key is valid if we can't check

    os.environ[engine_name.upper() + '_API_KEY'] = api_key
    try:
        # Attempt a simple completion to validate the API key
        completion(
            model=model_name,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        return True
    except Exception as e:
        logger.error(f"API key validation failed for {engine_name}: {str(e)}")
        return False


def get_enabled_engines_and_models():
    enabled_engines = []
    enabled_tiers = config['settings'].get('enabled_tiers', [])
    all_models_enabled = config['settings'].get('all_models_enabled', False)
    
    for engine in engine_config['engines']:
        api_key = os.getenv(engine['api_key_name'])
        if api_key:
            enabled_models = [model for model in engine['models'] if all_models_enabled or model['tier'] in enabled_tiers]
            if enabled_models:
                enabled_engines.append({
                    'name': engine['name'],
                    'models': enabled_models,
                    'api_key': api_key,
                    'default_model': engine['default_model']
                })
                logger.info(f"Found configuration for engine: {engine['name']} with {len(enabled_models)} model(s)")
    
    return enabled_engines

def select_and_validate_engine_and_model():
    enabled_engines = get_enabled_engines_and_models()
    if not enabled_engines:
        raise ValueError("No enabled engines found in configuration. Please check your API keys and enabled providers.")
    
    while enabled_engines:
        engine = random.choice(enabled_engines)
        model = random.choice(engine['models'])
        
        if validate_api_key(engine['name'], engine['default_model'], engine['api_key']):
            logger.info(f"Selected and validated engine: {engine['name']}, model: {model['name']}")
            return engine['name'], model['name'], model['temperature'], model['supports_system_role']
        
        enabled_engines.remove(engine)
    
    raise ValueError("No enabled engines with valid API keys found. Please check your configuration and API keys.")

# Select engine and model once at the start
try:
    ENGINE_NAME, MODEL_NAME, TEMPERATURE, SUPPORTS_SYSTEM_ROLE = select_and_validate_engine_and_model()
except ValueError as e:
    logger.error(str(e))
    ENGINE_NAME, MODEL_NAME, TEMPERATURE, SUPPORTS_SYSTEM_ROLE = None, None, None, None

# Set max tokens for messages
MAX_TOKENS_DAILY = 150
MAX_TOKENS_FOLLOW_UP = 100

# Make sure to export all necessary variables
__all__ = ['config', 'engine_config', 'ENGINE_NAME', 'MODEL_NAME', 'TEMPERATURE', 'SUPPORTS_SYSTEM_ROLE', 
           'FALLBACK_MESSAGES', 'TEAM_MEMBERS', 'SLACK_CHANNEL', 'DAILY_MESSAGE_PROMPT', 
           'FOLLOW_UP_MESSAGE_PROMPT', 'MAX_TOKENS_DAILY', 'MAX_TOKENS_FOLLOW_UP', 'SKIP_SLACK_POSTING', 'SLACK_BOT_TOKEN']
