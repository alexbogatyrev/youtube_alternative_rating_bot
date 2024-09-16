import unittest
from sentiment_analyzer import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Инициализируем SentimentAnalyzer с той же моделью, что и в основном коде
        cls.analyzer = SentimentAnalyzer()

    def test_analyze_positive(self):
        """Тест анализа положительного текста."""
        texts = ['I love this video!']
        results = self.analyzer.analyze(texts)
        self.assertIn(results[0]['stars'], [4, 5])

    def test_analyze_negative(self):
        """Тест анализа негативного текста."""
        texts = ['This is the worst video ever.']
        results = self.analyzer.analyze(texts)
        self.assertIn(results[0]['stars'], [1, 2])

    def test_analyze_neutral(self):
        """Тест анализа нейтрального текста."""
        texts = ['It is an average video.']
        results = self.analyzer.analyze(texts)
        self.assertIn(results[0]['stars'], [3])

if __name__ == '__main__':
    unittest.main()
