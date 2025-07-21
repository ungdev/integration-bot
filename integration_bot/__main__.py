import os
from pathlib import Path
from dotenv import load_dotenv
from integration_bot.bot import Bot

def main() -> None:
  # Load environment variables from .env file
  if Path('.env').is_file():
    load_dotenv()

  # Create an instance of the Bot class
  client = Bot()

  # Start the bot
  client.run(os.getenv('BOT_TOKEN'), reconnect=True)
  
if __name__ == '__main__':
	main()
