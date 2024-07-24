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

def get_random_engine_and_model():
    enabled_engines = [engine for engine in engine_config['engines'] if engine.get('enabled', True)]
    if not enabled_engines:
        raise ValueError("No enabled engines found in configuration")
    
    engine = random.choice(enabled_engines)
    model = random.choice(engine['models'])
    return engine['name'], model['name'], model['temperature'], model['supports_system_role']

# Extract relevant engine and model settings
ENGINE_NAME, MODEL_NAME, TEMPERATURE, SUPPORTS_SYSTEM_ROLE = get_random_engine_and_model()

# Set max tokens for messages
MAX_TOKENS_DAILY = 150
MAX_TOKENS_FOLLOW_UP = 100
