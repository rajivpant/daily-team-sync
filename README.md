# Daily Team Sync

DailyTeamSync is a Python application developed by [Rajiv Pant](https://rajiv.com/) that posts dynamic daily standup messages to Slack channels using language model AI for generating message variations. It includes motivational content and tasteful humor to keep your team engaged. It includes personalized follow-ups for team members.

## Features
- Dynamic daily standup message generation using a language model AI
- Motivational quotes, jokes, or fun facts included in daily messages
- Personalized follow-up messages for team members
- Fallback to predefined messages if the LLM API is unavailable

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
   cp example.env .env
   # Update the .env file with your OpenAI API key and Slack bot token
   ```

5. **Create and update `config.yaml`:**
   ```sh
   cp example-config.yaml config.yaml
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
Your code contributions are welcome. Please fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.

