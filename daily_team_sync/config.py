import os
import yaml
from dotenv import load_dotenv

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the project root directory
project_root = os.path.dirname(current_dir)

# Load environment variables from .env file
load_dotenv(os.path.join(project_root, '.env'))

# Set API keys from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
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

# Extract relevant engine and model settings
engine = next(e for e in engine_config['engines'] if e['name'] == 'openai')
default_model = next(m for m in engine['models'] if m['name'] == 'gpt-4o-mini')
MODEL_NAME = default_model['name']
TEMPERATURE = default_model['temperature']
