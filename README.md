# Daily Team Sync

Daily Team Sync is a Python application developed by [Rajiv Pant](https://rajiv.com/) that posts dynamic daily standup messages to Slack channels using language model AI for generating message variations. It includes motivational content and tasteful humor to keep your team engaged. It includes personalized follow-ups for team members.

## Blog Post
Ever imagined an AI that doesn't try to think for you, but instead inspires you to think better? In my latest blog post, I introduce Daily Team Sync, an open-source tool that's flipping the script on AI in the workplace. Instead of replacing human communication, this AI acts as a digital facilitator, sparking more engaging and productive team discussions. It's not about AI generating our thoughts, but about AI prompting us to share our human insights more effectively. Curious how this could transform your team's daily standups and overall dynamics? Dive into the full post to explore how we're using AI to make work more human, not less. You might just find the future of team collaboration hidden in the spaces between AI prompts and human responses. Read the blog post announceing Daily Team Sync at
[rajiv.com/blog/2024/07/21/facilitating-team-communication-by-ai-prompting-humans-introducing-daily-team-sync/](https://rajiv.com/blog/2024/07/21/facilitating-team-communication-by-ai-prompting-humans-introducing-daily-team-sync/)

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
     - "JohnDoe"
     - "JaneSmith"
     # Add more team members...

   slack:
     channel: "#daily-standup"  # Replace with your actual channel name
   ```

8. **Run the script:**
   ```sh
   python -m daily_team_sync.main
   ```

## Scheduling Automatic Runs

To run Daily Team Sync automatically at a scheduled time, you can use cron (on Unix-based systems) or Task Scheduler (on Windows).

### Using cron (Unix/Linux/macOS):

1. Open your crontab file:
   ```sh
   crontab -e
   ```

2. Add a line to schedule the script. For example, to run it every weekday at 8:30 AM:
   ```
   PYTHONPATH=/path/to/daily-team-sync
   30 8 * * 1-5 /path/to/your/venv/bin/python /path/to/daily-team-sync/daily_team_sync/main.py >> /path/to/daily-team-sync.log 2>&1
   ```

   Replace the following:
   - `/path/to/daily-team-sync` with the full path to your project directory
   - `/path/to/your/venv/bin/python` with the actual path to the Python interpreter in your virtual environment
   - `/path/to/daily-team-sync/daily_team_sync/main.py` with the full path to the `main.py` file
   - `/path/to/daily-team-sync.log` with the full path where you want to store the log file

3. Make sure the script has the necessary permissions to run:
   ```sh
   chmod +x /path/to/daily-team-sync/daily_team_sync/main.py
   ```

4. If you're using a virtual environment, you may need to activate it in the cron job. You can do this by adding the activation command before running the script:
   ```
   PYTHONPATH=/path/to/daily-team-sync
   30 8 * * 1-5 source /path/to/your/venv/bin/activate && python /path/to/daily-team-sync/daily_team_sync/main.py >> /path/to/daily-team-sync.log 2>&1
   ```

5. Ensure that all file paths in your configuration files (like .env and config.yaml) use absolute paths.

### Using Task Scheduler (Windows):

1. Open Task Scheduler
2. Click "Create Basic Task"
3. Name the task and set the trigger (e.g., daily at 8:30 AM)
4. For the action, choose "Start a program"
5. Set the program/script to your Python executable in the virtual environment
6. Set the arguments to the path of your main.py script
7. Set the "Start in" directory to your project directory

Remember to ensure that your machine is running and connected to the internet at the scheduled time for the script to execute successfully.

## Configuration
- **.env:** Contains API keys and tokens.
- **config.yaml:** Contains fallback messages, Slack usernames of team members, and the Slack channel name.

## Troubleshooting

If you encounter issues when running the script from cron, try the following:

1. Ensure all paths (including those in .env and config.yaml) are absolute paths.
2. Check the permissions of your script and configuration files.
3. If using a virtual environment, make sure to activate it before running the script.
4. Add logging to the script to help diagnose issues:

   ```python
   import logging
   logging.basicConfig(filename='/path/to/daily-team-sync.log', level=logging.DEBUG)
   ```

   Add log messages throughout the script to track its progress.

5. You can also redirect the script's output to a file in your cron job:
   ```
   30 8 * * 1-5 /path/to/your/venv/bin/python /path/to/daily-team-sync/daily_team_sync/main.py >> /path/to/daily-team-sync.log 2>&1
   ```

   This will capture both standard output and error messages in the log file.

## Contributing
Your code contributions are welcome. Please fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.
