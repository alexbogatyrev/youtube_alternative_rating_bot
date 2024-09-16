import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path

class SentimentAnalyzer:
    """
    Класс для анализа тональности текста с использованием модели Hugging Face и кешированием.
    """

    def __init__(self, model_name='nlptown/bert-base-multilingual-uncased-sentiment', cache_dir=None):
        """
        Инициализация пайплайна для анализа тональности.

        :param model_name: Название модели на Hugging Face.
        :param cache_dir: Директория для кеширования модели.
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent / 'model_cache'

        os.makedirs(cache_dir, exist_ok=True)

        # Загрузка токенизатора и модели с использованием cache_dir
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir, clean_up_tokenization_spaces=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, cache_dir=cache_dir)

        # Создание пайплайна анализа тональности без параметра clean_up_tokenization_spaces
        self.analyzer = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

    def analyze(self, texts):
        """
        Анализ списка текстов.

        :param texts: Список строк для анализа.
        :return: Список результатов анализа.
        """
        results = []
        for text in texts:
            result = self.analyzer(text[:512])[0]  # Ограничение длины текста до 512 символов
            label = result['label']  # Метка в формате '1 star', '2 stars', и т.д.
            stars = int(label.split()[0])  # Извлекаем числовое значение звезд
            results.append({
                'text': text,
                'stars': stars,
                'score': result['score']
            })
        return results
