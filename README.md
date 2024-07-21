# Daily Team Sync

DailyTeamSync is a Python application developed by [Rajiv Pant](https://rajiv.com/) that posts dynamic daily standup messages to Slack channels using language model AI for generating message variations. It includes motivational content and tasteful humor to keep your team engaged. It includes personalized follow-ups for team members.

## Features
- Dynamic daily standup message generation using a language model AI
- Motivational quotes, jokes, or fun facts included in daily messages
- Personalized follow-up messages for team members
- Fallback to predefined messages if the LLM API is unavailable

## Prerequisites
- Python 3.7 or higher
- A Slack workspace where you have permissions to add apps
- An OpenAI account for API access

## Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/daily-team-sync.git
   cd daily-team-sync
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Obtain an OpenAI API key:**
   - Go to [OpenAI's website](https://openai.com/) and sign up for an account if you don't have one.
   - Navigate to the [API keys page](https://platform.openai.com/account/api-keys) in your account settings.
   - Click on "Create new secret key" and copy the generated key.

5. **Set up a Slack bot:**
   - Go to [Slack's API website](https://api.slack.com/apps) and click "Create New App".
   - Choose "From scratch" and give your app a name and select your workspace.
   - Under "Add features and functionality", select "Bots".
   - Click "Add a Bot User" and fill in the details for your bot.
   - Go to "OAuth & Permissions" in the sidebar and scroll to "Scopes". Add the following Bot Token Scopes:
     - `chat:write`
     - `chat:write.public`
   - At the top of the "OAuth & Permissions" page, click "Install to Workspace".
   - After installation, you'll see a "Bot User OAuth Access Token". Copy this token.

6. **Create and populate the `.env` file:**
   ```sh
   cp example.env .env
   ```
   Edit the `.env` file and add your OpenAI API key and Slack bot token:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SLACK_BOT_TOKEN=your_slack_bot_token_here
   ```

7. **Create and update `config.yaml`:**
   ```sh
   cp example-config.yaml config.yaml
   ```
   Edit `config.yaml` to add your fallback messages, team members, and Slack channel:
   ```yaml
   fallback_messages:
     - "Good morning! Please share your progress, today's tasks, and any hurdles you're facing."
     # Add more fallback messages...

   team_members:
     - "@JohnDoe"
     - "@JaneSmith"
     # Add more team members...

   slack:
     channel: "#daily-standup"  # Replace with your actual channel name
   ```

8. **Run the script:**
   ```sh
   python -m daily_team_sync.main
   ```

## Scheduling Automatic Runs

To run DailyTeamSync automatically at a scheduled time, you can use cron (on Unix-based systems) or Task Scheduler (on Windows).

### Using cron (Unix/Linux/macOS):

1. Open your crontab file:
   ```sh
   crontab -e
   ```

2. Add a line to schedule the script. For example, to run it every weekday at 9:30 AM:
   ```
   30 9 * * 1-5 /path/to/your/venv/bin/python /path/to/daily-team-sync/daily_team_sync/main.py
   ```

### Using Task Scheduler (Windows):

1. Open Task Scheduler
2. Click "Create Basic Task"
3. Name the task and set the trigger (e.g., daily at 9:30 AM)
4. For the action, choose "Start a program"
5. Set the program/script to your Python executable in the virtual environment
6. Set the arguments to the path of your main.py script
7. Set the "Start in" directory to your project directory

Remember to ensure that your machine is running and connected to the internet at the scheduled time for the script to execute successfully.

## Configuration
- **.env:** Contains API keys and tokens.
- **config.yaml:** Contains fallback messages, Slack usernames of team members, and the Slack channel name.

## Contributing
Your code contributions are welcome. Please fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.
