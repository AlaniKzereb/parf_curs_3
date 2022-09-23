import json
from json import JSONDecodeError

from bp_posts.dao.comment import Comment

from exceptions.data_exceptions import DataSourceError

class CommentDAO:
    """Менеджер комментариев"""
    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """ преобразовывает строку JSON в объект Python """
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                comments_data = json.load(f)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f'Не удается получить данные из файла {self.path}')

        return comments_data


    def _load_comments(self):
        """возвращает список экземпляров"""

        comments_data = self._load_data()
        list_of_comments = [Comment(**comment_data) for comment_data in comments_data]
        return list_of_comments



    def get_comments_by_post_id(self, pk: int) -> list[Comment]:
        """возвращает комментарии определенного поста.
    Функция должна вызывать ошибку `ValueError`
    если такого поста нет и пустой список, если у поста нет комментов. """
        comments: list[Comment] = self._load_comments()
        comments_match: list[Comment] = [c for c in comments if c.pk == pk]
        return comments_match

