import unittest
import os
from telegram_bot import TelegramBot
from dotenv import load_dotenv

class TestExtractVideoID(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Загрузка переменных окружения
        load_dotenv()
        telegram_token = os.getenv('TELEGRAM_TOKEN', 'test_token')
        youtube_api_key = os.getenv('YOUTUBE_API_KEY', 'test_api_key')

        # Инициализируем бота
        cls.bot = TelegramBot(telegram_token, youtube_api_key)

    def test_valid_url(self):
        """Тест стандартной ссылки YouTube."""
        url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        video_id = self.bot._extract_video_id(url)
        self.assertEqual(video_id, 'dQw4w9WgXcQ')

    def test_short_url(self):
        """Тест короткой ссылки YouTube."""
        url = 'https://youtu.be/dQw4w9WgXcQ'
        video_id = self.bot._extract_video_id(url)
        self.assertEqual(video_id, 'dQw4w9WgXcQ')

    def test_url_with_additional_params(self):
        """Тест ссылки с дополнительными параметрами."""
        url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s'
        video_id = self.bot._extract_video_id(url)
        self.assertEqual(video_id, 'dQw4w9WgXcQ')

    def test_invalid_url(self):
        """Тест некорректной ссылки."""
        url = 'https://www.example.com/'
        video_id = self.bot._extract_video_id(url)
        self.assertIsNone(video_id)

    def test_empty_url(self):
        """Тест пустой строки."""
        url = ''
        video_id = self.bot._extract_video_id(url)
        self.assertIsNone(video_id)

if __name__ == '__main__':
    unittest.main()
