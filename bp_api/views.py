import logging

from flask import Blueprint, jsonify, abort

from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO
from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS

bp_api = Blueprint("bp_api", __name__)

post_dao = PostDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)

api_logger = logging.getLogger("api_logger")

@bp_api.route('/')
def api_posts_hello():

    return "Это api"


@bp_api.route('/posts/')
def api_posts_all():
    """Эндпоинт всех постов"""
    all_posts = post_dao.get_posts_all()
    all_posts_as_dict = [post.as_dict() for post in all_posts]
    api_logger.debug("All posts")
    return jsonify(all_posts_as_dict), 200

@bp_api.route('/posts/<int:postid>/')
def api_post(postid: int):
    """Эндпоинт для 1 поста"""
    post = post_dao.get_post_by_pk(postid)
    if post is None:
        api_logger.debug(f"Обращение к несуществующему посту {postid}")
        abort(404)
    api_logger.debug(f"Поста  {postid} не существует")
    return jsonify(post.as_dict()), 200

@bp_api.errorhandler(404)
def api_error(error):
    api_logger.error(f"Ошибка {error}")
    return jsonify({"error": str(error)}), 404