from flask import Flask, Blueprint, render_template

from bp_api.views import bp_api
from bp_posts.views import bp_posts
import config_logger
from exceptions.data_exceptions import DataSourceError


def create_and_config_app(config_path):
    app = Flask(__name__)
    app.register_blueprint(bp_posts)
    app.register_blueprint(bp_api, url_prefix='/api')
    app.config.from_pyfile(config_path)
    config_logger.config(app)

    return app

app = create_and_config_app("config.py")

@app.errorhandler(404)
def page_error_handler_404(error):
    return f"Страница не найдена: {error}", 404

@app.errorhandler(500)
def page_error_handler_500(error):
    return f"На сервере ошибка {error}", 500

@app.errorhandler(DataSourceError)
def page_error_handler_data_surce_error(error):
    return f"Ошибка данных {error}", 500

if __name__ == '__main__':
    app.run()
