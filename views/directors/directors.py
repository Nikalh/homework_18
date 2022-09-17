from flask_restx import Resource, Namespace
from flask import request
from setup_db import db
from models import Director, DirectorSchema

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
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
            movie.name  = req_json.get("name")
            db.session.add(movie)
            db.session.commit()
            return "Данные обновлены", 204
        except Exception as e:
            print(e)
            db.session.rollback()
            return "Неудачное обновление", 500

    # Удаляем режиссера с определенным запросом
    def delete(self,idx):
        movie = Director.query.get(idx)
        db.session.delete(movie)
        db.session.commit()
        return "Данные удалены", 204
