# Это файл конфигурации приложения, здесь может хранится путь к бд, ключ шифрования, что-то еще.
class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
