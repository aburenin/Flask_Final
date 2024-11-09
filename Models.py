import datetime
import os

from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from config import pakets, qa_list
from flask import request

# from app import login_manager

db = SQLAlchemy()
bcrypt = Bcrypt()

class Project():
    def __init__(self, username):
        self.username = username


class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, unique=True)
    fotos_list = db.Column(db.Text(5000), nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, password, date):
        self.name = name
        self.password = password
        self.date = date

    def __repr__(self):
        return f'{self.name}'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'fotos_list': self.fotos_list,
            'date': self.date.isoformat() if self.date else None
        }

    @classmethod
    def add_new_project(cls, app):
        with app.app_context():
            project_name = request.form.get('projectName')

            # Проверка, существует ли уже такой проект
            existing_project = Client.query.filter_by(name=project_name).first()
            if existing_project:
                return {'status': 'warning', 'text': f'{project_name} уже существует. Имя должно быть уникальным.'}

            try:
                # Если проекта не существует, продолжаем добавление
                # Password
                project_password = request.form.get('projectPassword')  # Get password from request form
                project_password_hash = bcrypt.generate_password_hash(project_password).decode('utf-8')
                # Date
                project_date = request.form.get('projectDate').replace('.', '-')  # Get date from request form
                date_object = datetime.datetime.strptime(project_date, '%d-%m-%Y')
                # New Project
                new_project = Client(name=project_name, password=project_password_hash, date=date_object)

                db.session.add(new_project)
                db.session.commit()

                return {'status': 'success', 'text': f'Проект с именем {project_name} создан.'}
            except Exception as e:
                return {'status': 'error', 'text': f'{e}'}

    @classmethod
    def change_project_password(cls, app):
        with app.app_context():
            project_name = request.form.get('projectName')
            existing_project = Client.query.filter_by(name=project_name).first()

            if existing_project:
                project_password = request.form.get('projectPassword')

                project_password_hash = bcrypt.generate_password_hash(project_password).decode('utf-8')
                existing_project.password = project_password_hash

                db.session.commit()
                return {'status': 'success', 'text': f'Пароль для {project_name} изменен.'}

            else:
                return {'status': 'info', 'text': 'Проекта не существует, обратитесь к администратору.'}


class Preise(db.Model):
    __tablename__ = 'preise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    @classmethod
    def check_db(cls, app):
        with app.app_context():
            for name, price, description in pakets:
                exist_paket = Preise.query.filter_by(name=name).first()

                if exist_paket:
                    change = False
                    if exist_paket.price != price:
                        change = True
                        exist_paket.price = price
                    if exist_paket.description != description:
                        change = True
                        exist_paket.description = description

                    if change:
                        db.session.commit()
                else:
                    # Создаем новый пакет
                    new_paket = Preise(name=name, price=price, description=description)
                    Preise.new_paket(new_paket, app)

    @classmethod
    def new_paket(cls, new_paket, app):
        with app.app_context():
            try:
                db.session.add(new_paket)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Ошибка при добавлении нового пакета: {e}")


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False, unique=True)
    answer = db.Column(db.Text(1000), nullable=False)

    def __init__(self, id, question, answer):
        self.id = id
        self.question = question
        self.answer = answer

    @classmethod
    def check_db(cls, app):
        with app.app_context():
            for id, question, answer in qa_list:
                exist_qa = Question.query.filter_by(id=id).first()

                if exist_qa:
                    change = False
                    if exist_qa.question != question:
                        change = True
                        exist_qa.question = question
                    if exist_qa.answer != answer:
                        change = True
                        exist_qa.answer = answer

                    if change:
                        db.session.commit()
                else:
                    new_question = Question(id=id, question=question, answer=answer)
                    Question.new_question(new_question, app)

    @classmethod
    def new_question(cls, new_question, app):
        with app.app_context():
            try:
                db.session.add(new_question)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Ошибка при добавлении нового пакета: {e}")


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
