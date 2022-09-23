import pytest

from main import app

class TestApi:

    post_keys = {"pk", "poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count"}

    @pytest.fixture
    def app_instance(self):
        return app.test_client()

    def test_all_posts_has_correct_status(self, app_instance):
        result = app_instance.get("/api/posts", follow_redirects=True)
        assert result.status_code == 200

    def test_all_posts_has_correct_keys(self, app_instance):
        result = app_instance.get("/api/posts", follow_redirects=True)
        list_of_posts = result.get_json()

        for post in list_of_posts:
            assert post.keys() == self.post_keys, "Неправильные ключи у словаря"



    def test_single_posts_has_correct_status(self, app_instance):
        result = app_instance.get("/api/posts/1", follow_redirects=True)
        assert result.status_code == 200


    def test_single_post_not_existent(self, app_instance):
        result = app_instance.get("/api/posts/100", follow_redirects=True)
        assert result.status_code == 404


    def test_single_post_has_correct_keys(self, app_instance):
        result = app_instance.get("/api/posts/1", follow_redirects=True)
        post = result.get_json()
        post_keys = set(post.keys())
        assert post_keys == self.post_keys


    @pytest.mark.parametrize("postid", [(1), (2), (3), (4)])
    def test_single_post_has_correct_data(self, app_instance, postid):
        result = app_instance.get(f"/api/posts/{postid}", follow_redirects=True)
        post = result.get_json()
        assert post["postid"] == postid, f"Неправильный id-номер при запросе  поста {postid}"
