from sqlalchemy import String, Integer, Column, Float, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

db = SQLAlchemy(model_class=Base)

def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=True)
    senha = db.Column(db.String(100), nullable=False)

class Produtos(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(100), nullable=True)
    preco = db.Column(db.Float, nullable=False, default= 0.0)
    quantia = db.Column(db.Integer, nullable=True)

class Livros(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), nullable=True, unique=True)
    editora = db.Column(db.String(100), nullable=True)
    ano_publicacao = db.Column(db.Integer, nullable=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
