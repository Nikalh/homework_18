# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
from flask import Flask
from flask_restx import Api

from config import Config
from views.directors.directors import director_ns
from views.genres.genres import genre_ns
from views.movies.movies import movie_ns
from setup_db import db


# функция создания основного объекта app
def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.app_context().push()
    return app


# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    create_data(app, db)


# функция создания таблиц с данными
def create_data(app, db):
    with app.app_context():
        db.create_all()



if __name__ == '__main__':
    app = create_app(Config())
    register_extensions(app)
    app.debug = True
    app.run(host="localhost", port=10001)
