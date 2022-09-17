from flask_restx import Resource, Namespace
from flask import request
from setup_db import db
from models import Genre, GenreSchema


genre_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        result = Genre.query.all()
        genres = genres_schema.dump(result)
        return genres

        # Добавляем новый жанр
    def post(self):
        data = request.json
        try:
            db.session.add(Genre(**data))
            db.session.commit()
            return "Данные успешно добавлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Неудача", 500

# Возвращаем только информацию о жанре с перечислением списка фильмов по жанру
@genre_ns.route('/<int:idx>')
class GenreView(Resource):
    def get(self, idx):
        genre = Genre.query.get(idx)
        return genre_schema.dump(genre), 200

    # Обновляем данные жанра с определенным запросом
    def put(self, idx):
        movie = Director.query.get(idx)
        req_json = request.json
        try:
            movie.name  = req_json.get("name")
            db.session.add(movie)
            db.session.commit()
            return "Данные обновлены", 204
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Неудачное обновление", 500

    # Удаляем жанр с определенным запросом
    def delete(self,idx):
        movie = Director.query.get(idx)
        db.session.delete(movie)
        db.session.commit()
        return "Данные удалены", 204

