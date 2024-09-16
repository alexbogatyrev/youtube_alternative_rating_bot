import unittest
from video_evaluator import VideoEvaluator

class TestVideoEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = VideoEvaluator()

    def test_evaluate_high_relevance(self):
        """Тест видео с высокой релевантностью."""
        comments = [
            {'stars': 5, 'likeCount': 10},
            {'stars': 5, 'likeCount': 5},
            {'stars': 4, 'likeCount': 20},
        ]
        result = self.evaluator.evaluate(comments)
        self.assertGreaterEqual(result['video_relevance'], 80)
        self.assertEqual(result['verdict'], 'Высокая релевантность')

    def test_evaluate_low_relevance(self):
        """Тест видео с низкой релевантностью."""
        comments = [
            {'stars': 1, 'likeCount': 5},
            {'stars': 2, 'likeCount': 2},
            {'stars': 1, 'likeCount': 1},
        ]
        result = self.evaluator.evaluate(comments)
        self.assertLessEqual(result['video_relevance'], 30)
        self.assertEqual(result['verdict'], 'Низкая релевантность')

    def test_evaluate_medium_relevance(self):
        """Тест видео со средней релевантностью."""
        comments = [
            {'stars': 5, 'likeCount': 10},
            {'stars': 3, 'likeCount': 5},
            {'stars': 1, 'likeCount': 10},
        ]
        result = self.evaluator.evaluate(comments)
        self.assertEqual(result['video_relevance'], 60)
        self.assertEqual(result['verdict'], 'Релевантное')

    def test_evaluate_no_likes(self):
        """Тест видео без лайков на комментариях."""
        comments = [
            {'stars': 3, 'likeCount': 0},
            {'stars': 3, 'likeCount': 0},
            {'stars': 3, 'likeCount': 0},
        ]
        result = self.evaluator.evaluate(comments)
        self.assertEqual(result['video_relevance'], 60)
        self.assertEqual(result['verdict'], 'Релевантное')

    def test_evaluate_no_comments(self):
        """Тест видео без комментариев."""
        comments = []
        result = self.evaluator.evaluate(comments)
        self.assertEqual(result['video_relevance'], 0)
        self.assertEqual(result['verdict'], 'Не релевантное')

if __name__ == '__main__':
    unittest.main()
