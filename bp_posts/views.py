from __future__ import annotations

from flask import Flask, Blueprint, render_template, request
from werkzeug.exceptions import abort

from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO
from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS

bp_posts = Blueprint("bp_posts", __name__, template_folder="templates")

post_dao = PostDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)

@bp_posts.route("/")
def posts_main_page():
    """Все посты"""
    all_posts = post_dao.get_posts_all()
    return render_template("posts_index.html", posts=all_posts)

@bp_posts.route("/posts/<postid>")
def post_page(postid):
    """один пост"""

    postid = int(postid)
    post: Post | None= post_dao.get_post_by_pk(postid)

    comments = comments_dao.get_comments_by_post_id(postid)

    comments_len = len(comments)

    if post is None:
        abort(404)

    return render_template('single_post.html', post=post, comments=comments, quantity=comments_len)
# РАЗОБРАТЬСЯБ ПОЧЕМУ ОШИБКА?
# ИМЕННО В КОММЕНТАХ


@bp_posts.route("/users/<username>")
def user_page(username):
    """страница постов конкретного пользователя"""
    posts = post_dao.get_posts_by_user(username)

    if posts == []:
        abort(404, "Пользователь не найден")

    return render_template("posts_user-feed.html", posts=posts, user_name=username)

@bp_posts.route("/search/")
def search_page():
    "Страница поиска по слову"
    query = request.args.get("s", "")
    if query == "":
        posts = []
    else:
        posts = post_dao.search_for_posts(query)

    return render_template("posts_search.html", posts=posts, query=query, posts_len=len(posts))




