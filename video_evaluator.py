class VideoEvaluator:
    """
    Класс для оценки релевантности видео на основе комментариев.
    """

    def evaluate(self, comments):
        """
        Вычисляет релевантность видео в процентах.

        :param comments: Список комментариев с метаданными, включая 'stars' и 'likeCount'.
        :return: Словарь с релевантностью и вердиктом.
        """
        total_weighted_relevance = 0
        total_weight = 0

        for comment in comments:
            stars = comment['stars']
            like_count = comment['likeCount']
            like_weight = like_count + 1  # Вес комментария

            # Релевантность комментария в процентах
            relevance = (stars / 5) * 100

            # Взвешенная релевантность
            weighted_relevance = relevance * like_weight

            total_weighted_relevance += weighted_relevance
            total_weight += like_weight

        if total_weight == 0:
            video_relevance = 0
        else:
            video_relevance = total_weighted_relevance / total_weight

        # Округляем релевантность до целого числа
        video_relevance = round(video_relevance)

        # Определяем вердикт на основе пороговых значений
        if video_relevance >= 80:
            verdict = 'Высокая релевантность'
        elif video_relevance >= 60:
            verdict = 'Релевантное'
        elif video_relevance >= 40:
            verdict = 'Средняя релевантность'
        elif video_relevance >= 20:
            verdict = 'Низкая релевантность'
        else:
            verdict = 'Не релевантное'

        return {
            'video_relevance': video_relevance,
            'verdict': verdict
        }
