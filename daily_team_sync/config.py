import os
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set API keys from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

# Load configuration from config.yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

FALLBACK_MESSAGES = config['fallback_messages']
TEAM_MEMBERS = config['team_members']
SLACK_CHANNEL = config['slack']['channel']

# Load engine settings from engines.yaml
with open('engines.yaml', 'r') as file:
    engine_config = yaml.safe_load(file)

# Extract relevant engine and model settings
engine = next(e for e in engine_config['engines'] if e['name'] == 'openai')
default_model = next(m for m in engine['models'] if m['name'] == 'gpt-4o-mini')
MODEL_NAME = default_model['name']
TEMPERATURE = default_model['temperature']