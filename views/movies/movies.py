from flask import request
from flask_restx import Resource, Namespace

from models import Movie, MovieSchema
from setup_db import db

movie_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# Возвращаем список всех фильмов
@movie_ns.route('/')
class MovieView(Resource):
    def get(self):
        result = Movie.query
        # movies = movies_schema.dump(result)
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        year = request.args.get("year")


        # Возвращаем только фильмы с определенным годом по запросу
        if year:
            result = result.filter(Movie.year == year)
            return movies_schema.dump(result.all()), 200

        # Возвращаем только фильмы с определенным режиссером по запросу
        if director_id:
            result = result.filter(Movie.director_id == director_id)

            # Возвращаем только фильмы с определенным жанром по запросу
        if genre_id:
            result = result.filter(Movie.genre_id == genre_id)
        return movies_schema.dump(result.all()), 200

        # Возвращаем только фильмы с определенным годом по запросу
        # if year:
        #     result = result.filter(Movie.year == year)
        # return movies_schema.dump(result.all()), 200

    # Добавляем новый фильм
    def post(self):
        data = request.json
        try:
            db.session.add(Movie(**data))
            db.session.commit()
            return "Данные успешно добавлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Неудача", 500


# Возвращаем подробную информацию о фильме
@movie_ns.route('/<int:idx>')
class MovieView(Resource):
    def get(self, idx):
        movie = Movie.query.get(idx)
        return movie_schema.dump(movie)

    # Обновляем фильмы с определенным запросом
    def put(self, idx):
        movie = Movie.query.get(idx)
        req_json = request.json
        try:
            movie.title = req_json.get("title")
            movie.description = req_json.get("description")
            movie.trailer = req_json.get("trailer")
            movie.year = req_json.get('year')
            movie.rating = req_json.get('rating')
            movie.genre_id = req_json.get('genre_id')
            movie.director_id = req_json.get('director_id')
            db.session.add(movie)
            db.session.commit()
            return "Данные обновлены", 204
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Неудачное обновление", 500

    # Удаляем только фильм с определенным запросом
    def delete(self, idx):
        movie = Movie.query.get(idx)
        db.session.delete(movie)
        db.session.commit()
        return "Данные удалены", 204
