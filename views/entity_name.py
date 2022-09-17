# здесь контроллеры/хендлеры/представления для обработки запросов (flask ручки). сюда импортируются сервисы из пакета service

# Пример
from flask_restx import Resource

#
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


# book_ns = Namespace('books')
#
#
# @book_ns.route('/')
# class BooksView(Resource):
#     def get(self):
#         return "", 200
#
#     def post(self):
#         return "", 201

# Возвращаем список всех фильмов
@movie_ns.route('/')
class MovieView(Resource):
    def get(self):
        result = Movie.query

        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")

        # Возвращаем только фильмы с определенным режиссером по запросу
        if director_id:
            result = result.filter(Movie.director_id == director_id)

        # Возвращаем только фильмы с определенным жанром по запросу
        if genre_id:
            result = result.filter(Movie.genre_id == genre_id)
        return movies_schema.dump(result.all()), 200

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


# Возвращаем информацию о режиссерах
@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        result = Director.query.all()
        directors = directors_schema.dump(result)
        return directors

    # Добавляем нового режиссера
    def post(self):
        data = request.json
        try:
            db.session.add(Director(**data))
            db.session.commit()
            return "Данные успешно добавлены", 201
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Неудача", 500


# Возвращаем только подробную информацию о режиссере
@director_ns.route('/<int:idx>')
class DirectorView(Resource):
    def get(self, idx):
        director = Director.query.get(idx)
        return director_schema.dump(director)

    # Обновляем данные режиссера с определенным запросом
    def put(self, idx):
        movie = Director.query.get(idx)
        req_json = request.json
        try:
            movie.name = req_json.get("name")
            db.session.add(movie)
            db.session.commit()
            return "Данные обновлены", 204
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Неудачное обновление", 500

    # Удаляем режиссера с определенным запросом
    def delete(self, idx):
        movie = Director.query.get(idx)
        db.session.delete(movie)
        db.session.commit()
        return "Данные удалены", 204


# Возвращаем все жанры
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
            movie.name = req_json.get("name")
            db.session.add(movie)
            db.session.commit()
            return "Данные обновлены", 204
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Неудачное обновление", 500

    # Удаляем жанр с определенным запросом
    def delete(self, idx):
        movie = Director.query.get(idx)
        db.session.delete(movie)
        db.session.commit()
        return "Данные удалены", 204
