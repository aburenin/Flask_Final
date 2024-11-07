import datetime
import os

from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# from app import login_manager

db = SQLAlchemy()
bcrypt = Bcrypt()


class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, unique=True)
    fotos_list = db.Column(db.Text(5000), nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'

    # Сериализатор для преобразования в словарь
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'fotos_list': self.fotos_list,
            'date': self.date.isoformat() if self.date else None
        }


class Preise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(500), nullable=False)

    def __repr__(self):
        return f'{self.name}'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False, unique=True)
    answer = db.Column(db.Text(1000), nullable=False)

    def __repr__(self):
        return f'{self.question}'


class UserDirectories:
    def __init__(self, username):
        self.username = username
        self.main_path = os.path.join('static', 'media', 'clients', self.username)
        self.small_path = os.path.join(self.main_path, 'small')
        self.blur_path = os.path.join(self.main_path, 'blur')

    def get_paths(self):
        return [self.main_path, self.small_path, self.blur_path]


class PortfolioDir:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.portfolio_main = os.path.join('static', 'media', self.portfolio)
        self.portfolio_small = os.path.join(self.portfolio_main, 'small')
        self.portfolio_blur = os.path.join(self.portfolio_main, 'blur')

    def get_paths(self):
        return [self.portfolio_main, self.portfolio_small, self.portfolio_blur]



