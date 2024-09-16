import os
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from pathlib import Path
from typing import List
from deep_translator import GoogleTranslator as DeepGoogleTranslator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Translator:
    """
    Класс для перевода текста на английский язык с использованием deep-translator и
    резервного переводчика на основе модели Hugging Face.
    """

    def __init__(self, model_name='Helsinki-NLP/opus-mt-mul-en', cache_dir=None):
        """
        Инициализация переводчиков.

        :param model_name: Название модели на Hugging Face.
        :param cache_dir: Директория для кеширования модели.
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent / 'model_cache'

        os.makedirs(cache_dir, exist_ok=True)

        # Загрузка токенизатора и модели с использованием cache_dir
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=cache_dir)

        # Создание пайплайна перевода для резервного переводчика
        self.model_translator = pipeline('translation', model=model, tokenizer=tokenizer)

        # Инициализация основного переводчика с использованием deep-translator
        self.deep_translator = DeepGoogleTranslator(source='auto', target='en')

    def translate_with_model(self, texts: List[str]) -> List[str]:
        """
        Резервный метод перевода списка текстов на английский язык с использованием модели Hugging Face.

        :param texts: Список строк для перевода.
        :return: Список переведённых текстов.
        """
        translations = []
        for text in texts:
            # Ограничение длины текста до 512 символов
            translated = self.model_translator(text[:512], max_length=512)
            translations.append(translated[0]['translation_text'])
        return translations

    def translate(self, texts: List[str]) -> List[str]:
        """
        Переводит список текстов на английский язык, используя переводчик Hugging Face.
        """
        try:
            return self.translate_with_model(texts)
        except Exception as e:
            logger.error(f"Ошибка при переводе с помощью резервного переводчика: {e}")
            raise e

    #РЕЗЕРВ
    def __translate(self, texts: List[str]) -> List[str]:
        """
        Переводит список текстов на английский язык, используя deep-translator.
        При ошибке использует переводчик Hugging Face.
        """
        try:
            logger.info("Перевод с помощью deep-translator")
            translated_texts = []
            for idx, text in enumerate(texts):
                translated_text = self.deep_translator.translate(text)
                translated_texts.append(translated_text)
                logger.debug(f"Оригинал: {text}")
                logger.debug(f"Перевод: {translated_text}")
            return translated_texts
        except Exception as e:
            logger.error(f"Ошибка при переводе с помощью deep-translator: {e}")
            logger.info("Перевод с помощью резервного переводчика (Hugging Face Transformers)")
            # Используем резервный переводчик
            try:
                return self.translate_with_model(texts)
            except Exception as e:
                logger.error(f"Ошибка при переводе с помощью резервного переводчика: {e}")
                raise e

