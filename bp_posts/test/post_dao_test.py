import pytest

from bp_posts.dao import post_dao
from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO

def check_fields(post):
    fields = ["pk", "poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count"]

    for field in fields:
        assert hasattr(post, field), f"Нет поля {field}"



class TestPostDAO:

    @pytest.fixture
    def post_dao(self):
        post_dao_instance = PostDAO("./bp_posts/test/post_mock.json")
        return post_dao_instance

#тесты  на get_posts_all

    def test_get_posts_all_types(self, post_dao):

        posts = post_dao.get_posts_all()
        assert type(posts) == list, "Неверный тип результата"

        post = post_dao.get_posts_all()[0]
        assert type(post) == Post, "Неверный тип поста"

    def test_get_posts_all_fields(self, post_dao):
        posts = post_dao.get_posts_all()
        post = post_dao.get_posts_all()[0]

        check_fields(post)

    def test_get_posts_all_correct_id(self, post_dao):
        posts = post_dao.get_posts_all()
        correct_pks = {1,2,3}
        pks = set([post.pk for post in posts])

        assert pks == correct_pks, "Не совпадают полученные id"


#тесты на get_post_by_pk

    def test_get_post_by_pk_type(self, post_dao):
        post = post_dao.get_post_by_pk(1)
        assert type(post) == Post, "Неверный тип"


    def test_get_post_by_pk_dao_filds(self, post_dao):
        post = post_dao.get_post_by_pk(1)
        check_fields(post)


    def test_get_post_by_pk_none(self, post_dao):
        post = post_dao.get_post_by_pk(500)
        assert post is None, "Не существующий pk"


    @pytest.mark.parametrize("pk", [1, 2, 2])
    def test_get_post_by_pk_correct_id(self, post_dao, pk):
        post = post_dao.get_post_by_pk(pk)
        assert post.pk == pk, f"Неверный pk"


# тесты на search_for_posts
    def test_search_for_posts_fields(self, post_dao):
        posts = post_dao.search_for_posts("еда")
        assert type(posts) == list, "Неверный тип результата списка постов"
        post = post_dao.get_posts_all()[0]
        assert type(post) == Post, "Неверный тип результата поста"


    def test_search_for_posts_not_found(self, post_dao):
        posts = post_dao.search_for_posts("chjkj")
        assert posts == [], "посты не найдены, пустой список - []"

    @pytest.mark.parametrize("s, expected_pks", [
        ("опять", {1}),
        ("днем", {2}),
        ("на", {1,2,3}),
    ])
    def test_search_for_posts_result(self, post_dao, s, expected_pks):
        posts = post_dao.search_for_posts(s)
        pks = set({post.pk for post in posts})
        assert pks == expected_pks, f"Неверный результат поиска для {s}"

# тесты на get_posts_by_user


    # def test_get_posts_by_user_type(self, post_dao):
    #     posts = post_dao.get_posts_by_user("leo")
    #     assert type(posts) == list, "Неверный тип"
    #
    #
    # def test_get_posts_by_user_dao_filds(self, post_dao):
    #     posts = post_dao.get_posts_by_user("leo")
    #     check_fields(posts)
    #
    #
    # def test_get_posts_by_user_not_found(self, post_dao):
    #     posts = post_dao.get_posts_by_user("500")
    #     assert posts == [], "посты не найдены, пустой список - []"
    #
    #
    # @pytest.mark.parametrize("poster_name, expected_pks", [
    #     ("leo", {1}),
    #     ("johnny", {2}),
    #     ("hank", {3}),
    # ])
    # def test_get_posts_by_user_result(self, post_dao, poster_name, expected_pks):
    #     posts = post_dao.get_posts_by_user(poster_name)
    #     pks = set({post.pk for post in posts})
    #     assert pks == expected_pks, f"Неверный результат поиска для {poster_name}"



