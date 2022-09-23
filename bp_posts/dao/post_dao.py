import json
from json import JSONDecodeError


from bp_posts.dao.post import Post
from exceptions.data_exceptions import DataSourceError


class PostDAO:
    """Менеджер постов"""
    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """ преобразовывает строку JSON в объект Python """
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                posts_data = json.load(f)
        except(FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f'Не удается получить данные из файла {self.path}')

        return posts_data


    def _load_posts(self):
        """возвращает список экземпляров"""

        posts_data = self._load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data]
        return list_of_posts



    def get_posts_all(self):
        """возвращает посты списоком экземпляров"""
        posts = self._load_posts()
        return posts


    def get_post_by_pk(self, pk):
        """возвращает один пост по его идентификатору"""

        # if type(pk) != int:
        #     raise TypeError("pk - должен быть в виде числа")

        posts = self._load_posts()
        for post in posts:
            if post.pk == pk:
                return post


    def search_for_posts(self, query):
        """возвращает список постов по ключевому слову"""
        posts = self._load_posts()
        output_posts = []
        # output_posts = [post for post in posts if query.lower() in post.content.lower()]
        i = 1
        for post in posts:
            if i == 10:
                break
            if query.lower() in post.content.lower():
                i += 1
                output_posts.append(post)

        return output_posts




    def get_posts_by_user(self, user_name):
        """возвращает посты определенного пользователя.
Функция должна вызывать ошибку `ValueError` если такого
пользователя нет и пустой список, если у пользователя нет постов."""
        user_name = str(user_name).lower()
        posts = self._load_posts()
        output_posts = [post for post in posts if post.poster_name.lower() == user_name]
        return output_posts


    # def add_bookmark(self, postid):
    #     if postid == post.pk:
    #         with open('bookmarks.json', 'r', encoding='utf8') as f:
    #         data = json.load(f)
    #         data['bookmarks.json'].append(post)
    #         with open('bookmarks.json', 'w', encoding='utf8') as outfile:
    #             json.dump(data, outfile, ensure_ascii=False, indent=2)


