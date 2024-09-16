import unittest
import os
from youtube_service import YouTubeService
from dotenv import load_dotenv

class TestYouTubeService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Загрузка переменных окружения
        load_dotenv()
        youtube_api_key = os.getenv('YOUTUBE_API_KEY')

        if not youtube_api_key:
            raise ValueError("Необходимо установить YOUTUBE_API_KEY в файле .env для тестирования.")


        cls.service = YouTubeService(youtube_api_key)

    def test_get_comments(self):
        """Тест получения комментариев к реальному видео."""
        video_id = 'dQw4w9WgXcQ'  # Пример видео
        comments = self.service.get_comments(video_id, max_results=5)
        self.assertIsInstance(comments, list)
        self.assertGreater(len(comments), 0)
        self.assertIsInstance(comments[0], dict)
        self.assertIn('text', comments[0])
        self.assertIn('likeCount', comments[0])
        self.assertIsInstance(comments[0]['text'], str)
        self.assertIsInstance(comments[0]['likeCount'], int)

if __name__ == '__main__':
    unittest.main()
