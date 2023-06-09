from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .config import Config
import csv


db = SQLAlchemy()
DB_NAME = Config.DB_NAME


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(config.Config())
    db.init_app(app)

    from .views import Views
    from .auth import Auth

    app.register_blueprint(Views.views, url_prefix='/')
    app.register_blueprint(Auth.auth, url_prefix='/')

    from .models import User, Inventario, Vinhos, Vinicola
    
    with app.app_context():
        db.create_all()    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


