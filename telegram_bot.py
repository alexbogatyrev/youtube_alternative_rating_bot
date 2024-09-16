import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from youtube_service import YouTubeService
from sentiment_analyzer import SentimentAnalyzer
from translator import Translator
from video_evaluator import VideoEvaluator

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Фильтрация логов от сторонних библиотек
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('googleapiclient').setLevel(logging.WARNING)
logging.getLogger('transformers').setLevel(logging.WARNING)

# Обработчики для файла и консоли
file_handler = logging.FileHandler('bot.log', mode='a')
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Форматирование
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавление обработчиков
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class TelegramBot:
    """
    Класс для управления Telegram-ботом.
    """
    MAX_COMMENTS = 100
    MAX_MESSAGE_LENGTH = 4096  # Максимальная длина сообщения в Telegram

    def __init__(self, token, youtube_api_key):
        """
        Инициализация бота и необходимых сервисов.

        :param token: Токен Telegram бота.
        :param youtube_api_key: API ключ YouTube Data API.
        """
        self.token = token
        self.youtube_service = YouTubeService(youtube_api_key)
        self.translator = Translator()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.video_evaluator = VideoEvaluator()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start."""
        await update.message.reply_text(
            'Привет! Отправьте мне ссылку на YouTube видео, и я проведу анализ.'
        )

    async def analyze(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /analyze."""
        if not context.args:
            await update.message.reply_text('Пожалуйста, предоставьте ссылку на YouTube видео после команды /analyze.')
            return

        url = context.args[0]
        video_id = self._extract_video_id(url)

        if not video_id:
            await update.message.reply_text('Некорректная ссылка на видео. Пожалуйста, попробуйте снова.')
            return

        await self._process_video(update, video_id)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обрабатывает входящие текстовые сообщения."""
        message_text = update.message.text

        if len(message_text) > self.MAX_MESSAGE_LENGTH:
            await update.message.reply_text('Сообщение слишком длинное. Пожалуйста, отправьте более короткое сообщение.')
            return

        video_id = self._extract_video_id(message_text)

        if not video_id:
            await update.message.reply_text('Пожалуйста, отправьте корректную ссылку на YouTube видео.')
            return

        await self._process_video(update, video_id)

    async def _process_video(self, update: Update, video_id: str):
        """Обрабатывает анализ видео по идентификатору видео."""
        await update.message.reply_text('Получаю комментарии, пожалуйста, подождите...')

        comments = self._fetch_comments(video_id)
        if comments is None:
            await update.message.reply_text('Произошла ошибка при получении комментариев.')
            return
        if not comments:
            await update.message.reply_text('Не удалось найти комментарии к этому видео.')
            return

        await update.message.reply_text('Перевожу комментарии, это может занять некоторое время...')

        translated_texts = self._translate_comments([comment['text'] for comment in comments])
        if translated_texts is None:
            await update.message.reply_text('Произошла ошибка при переводе комментариев.')
            return

        await update.message.reply_text('Анализирую комментарии, это может занять некоторое время...')

        sentiments = self._analyze_sentiments(translated_texts)
        if sentiments is None:
            await update.message.reply_text('Произошла ошибка при анализе комментариев.')
            return

        # Обновляем комментарии с результатами анализа
        for i, comment in enumerate(comments):
            comment['translated_text'] = translated_texts[i]
            comment['stars'] = sentiments[i]['stars']
            comment['sentiment_score'] = sentiments[i]['score']

        # Оцениваем видео
        evaluation_result = self._evaluate_video(comments)

        # Отправляем результат пользователю
        await self._send_evaluation_result(update, evaluation_result)

    def _extract_video_id(self, url):
        """Извлекает идентификатор видео из ссылки YouTube."""
        logger.info(f"Извлечение video_id из URL: {url}")
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'youtu\.be\/([0-9A-Za-z_-]{11})'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                logger.info(f"Найден video_id: {video_id}")
                return video_id
        logger.warning("Не удалось извлечь video_id")
        return None

    def _fetch_comments(self, video_id):
        """Получает комментарии к видео."""
        logger.info(f"Получение комментариев для video_id: {video_id}")
        try:
            comments = self.youtube_service.get_comments(video_id, max_results=self.MAX_COMMENTS)
            logger.info(f"Получено {len(comments)} комментариев")
            return comments
        except Exception as e:
            logger.error(f"Ошибка при получении комментариев: {e}")
            return None

    def _translate_comments(self, texts):
        """Переводит комментарии на английский язык."""
        logger.info("Начало перевода комментариев")
        try:
            translated_texts = self.translator.translate(texts)
            logger.info("Перевод комментариев завершён")
            return translated_texts
        except Exception as e:
            logger.error(f"Ошибка при переводе комментариев: {e}")
            return None

    def _analyze_sentiments(self, texts):
        """Анализирует тональность переведённых комментариев."""
        logger.info("Начало анализа тональности комментариев")
        try:
            sentiments = self.sentiment_analyzer.analyze(texts)
            logger.info("Анализ тональности завершён")
            return sentiments
        except Exception as e:
            logger.error(f"Ошибка при анализе тональности: {e}")
            return None

    def _evaluate_video(self, comments):
        """Оценивает видео на основе комментариев."""
        logger.info("Начало оценки видео")
        evaluation_result = self.video_evaluator.evaluate(comments)
        logger.info(f"Оценка видео завершена: {evaluation_result}")
        return evaluation_result

    async def _send_evaluation_result(self, update: Update, evaluation_result):
        """Отправляет результат оценки видео пользователю."""
        relevance = evaluation_result['video_relevance']
        verdict = evaluation_result['verdict']

        response = (
            f'Анализ завершён!\n\n'
            f'Релевантность видео: {relevance}%\n'
            f'Видео считается: {verdict}'
        )

        await update.message.reply_text(response)

    def run(self):
        """Запуск бота."""
        application = ApplicationBuilder().token(self.token).build()

        application.add_handler(CommandHandler('start', self.start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        application.run_polling()