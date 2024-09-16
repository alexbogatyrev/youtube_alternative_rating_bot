import os
from telegram_bot import TelegramBot
from dotenv import load_dotenv

def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

    if not TELEGRAM_TOKEN or not YOUTUBE_API_KEY:
        raise ValueError("Необходимо установить TELEGRAM_TOKEN и YOUTUBE_API_KEY")

    bot = TelegramBot(TELEGRAM_TOKEN, YOUTUBE_API_KEY)
    bot.run()

if __name__ == '__main__':
    main()
