# Daily Team Sync

DailyTeamSync is a Python application developed by [Rajiv Pant](https://rajiv.com/) that posts dynamic daily standup messages to Slack channels using OpenAI's GPT-3 for generating message variations. It includes motivational content to keep your team engaged and personalized follow-ups for team members. 

## Features
- Dynamic daily standup message generation using OpenAI's GPT-3
- Motivational quotes, jokes, or fun facts included in daily messages
- Personalized follow-up messages for team members
- Fallback to predefined messages if OpenAI API is unavailable

## Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/daily-team-sync.git
   cd daily-team-sync
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Create and populate the `.env` file:**
   ```sh
   cp .env.example .env
   # Update the .env file with your OpenAI API key and Slack bot token
   ```

5. **Create and update `config.yaml`:**
   ```sh
   cp config.yaml.example config.yaml
   # Update config.yaml with your fallback messages and team members
   ```

6. **Run the script:**
   ```sh
   python -m daily_team_sync.main
   ```

## Configuration
- **.env:** Contains API keys and tokens.
- **config.yaml:** Contains fallback messages and Slack usernames of team members.

## Contributing
Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.

