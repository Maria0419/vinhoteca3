from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model): #model
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Vinhos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    safra = db.Column(db.Integer)
    tempodeguarda = db.Column(db.Integer)
    harmonizacao = db.Column(db.String(100))
    #adega_id = db.Column(db.String(100), db.ForeignKey('adega.id'))
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

vinho_inventario = db.Table('vinho_inventario',
    db.Column('vinho_id', db.Integer, db.ForeignKey('vinhos.id'), primary_key=True),
    db.Column('inventario_id', db.Integer, db.ForeignKey('inventario.id'), primary_key=True)
)

class Inventario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    localizacao = db.Column(db.String(100))
    estoque = db.Column(db.Integer)
    #vinho = db.relationship('Vinhos')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    inventario = db.relationship('Inventario')
