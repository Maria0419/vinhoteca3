from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Vinicola(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    regiao = db.Column(db.String(100))

class Vinhos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    safra = db.Column(db.Integer)
    uva = db.Column(db.String(100))
    tempodeguarda = db.Column(db.Integer)
    harmonizacao = db.Column(db.String(100))
    vinicola_id = db.Column(db.Integer, db.ForeignKey('vinicola.id'))

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    localizacao = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vinho_id = db.Column(db.Integer, db.ForeignKey('vinhos.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    inventario = db.relationship('Inventario')
