from googleapiclient.discovery import build
class YouTubeService:
    """
    Класс для взаимодействия с YouTube Data API.
    """

    def __init__(self, api_key):
        """
        Инициализация клиента YouTube API.

        :param api_key: API ключ для доступа к YouTube Data API.
        """
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.max_comments = 20

    def get_comments(self, video_id, max_results=100):
        """
        Получение комментариев к видео, включая вложенные комментарии, отсортированных по убыванию лайков.

        :param video_id: Идентификатор видео на YouTube.
        :param max_results: Максимальное количество комментариев для возвращения после обработки.
        :return: Список словарей с комментариями и их метаданными.
        """
        all_comments = []
        comments_fetched = 0
        total_comments_to_fetch = max_results * 2

        request = self.youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            maxResults=100,
            textFormat='plainText',
            order='relevance'
        )

        while request and comments_fetched < total_comments_to_fetch:
            response = request.execute()
            for item in response.get('items', []):
                # Верхнеуровневый комментарий
                top_comment_snippet = item['snippet']['topLevelComment']['snippet']
                comment_text = top_comment_snippet['textDisplay']
                like_count = top_comment_snippet.get('likeCount', 0)
                all_comments.append({
                    'text': comment_text,
                    'likeCount': like_count
                })
                comments_fetched += 1

                # Вложенные комментарии
                replies = item.get('replies', {}).get('comments', [])
                for reply in replies:
                    reply_snippet = reply['snippet']
                    reply_text = reply_snippet['textDisplay']
                    reply_like_count = reply_snippet.get('likeCount', 0)
                    all_comments.append({
                        'text': reply_text,
                        'likeCount': reply_like_count
                    })
                    comments_fetched += 1

            # Получение следующей страницы комментариев
            request = self.youtube.commentThreads().list_next(request, response)

        # Удаление дубликатов
        unique_comments = []
        seen_texts = set()
        for comment in all_comments:
            text = comment['text']
            if text not in seen_texts:
                seen_texts.add(text)
                unique_comments.append(comment)

        # Сортировка по количеству лайков
        unique_comments.sort(key=lambda x: x['likeCount'], reverse=True)

        # Возврат первых max_results комментариев
        #final_comments = unique_comments[:max_results]
        final_comments = unique_comments[:self.max_comments]

        return final_comments
