
class Config(object):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    DB_NAME = "database.db"
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_NAME}'
    SECRET_KEY = 'splashed_your_wine_into_me'
    