import os
import yaml
from dotenv import load_dotenv
import random

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

def get_enabled_engines_and_models():
    enabled_engines = []
    enabled_providers = config['settings'].get('enabled_providers', [])
    enabled_tiers = config['settings'].get('enabled_tiers', [])
    
    for engine in engine_config['engines']:
        if engine['name'] in enabled_providers and engine['api_key_name'] in os.environ:
            enabled_models = [model for model in engine['models'] if model['tier'] in enabled_tiers]
            if enabled_models:
                enabled_engines.append({
                    'name': engine['name'],
                    'models': enabled_models
                })
    return enabled_engines

def select_engine_and_model():
    enabled_engines = get_enabled_engines_and_models()
    if not enabled_engines:
        raise ValueError("No enabled engines found in configuration")
    
    engine = random.choice(enabled_engines)
    model = random.choice(engine['models'])
    return engine['name'], model['name'], model['temperature'], model['supports_system_role']

# Select engine and model once at the start
ENGINE_NAME, MODEL_NAME, TEMPERATURE, SUPPORTS_SYSTEM_ROLE = select_engine_and_model()

# Set max tokens for messages
MAX_TOKENS_DAILY = 150
MAX_TOKENS_FOLLOW_UP = 100

# Export engine_config
__all__ = ['config', 'engine_config', 'ENGINE_NAME', 'MODEL_NAME', 'TEMPERATURE', 'SUPPORTS_SYSTEM_ROLE', 
           'FALLBACK_MESSAGES', 'TEAM_MEMBERS', 'SLACK_CHANNEL', 'DAILY_MESSAGE_PROMPT', 
           'FOLLOW_UP_MESSAGE_PROMPT', 'MAX_TOKENS_DAILY', 'MAX_TOKENS_FOLLOW_UP']
