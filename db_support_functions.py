import os
from datetime import datetime

from Models import db, Preise, Question, Client, bcrypt
from config import qa_list

from flask import jsonify, request, Flask


def check_db_instance(app):
    if not os.path.exists('instance/fotos-baby.db'):
        with app.app_context():
            db.create_all()
    Preise.checkDB(app=app)
    Question.checkDB(app=app)


def add_new_project(app):
    with app.app_context():
        project_name = request.form.get('projectName')
        project_password = request.form.get('projectPassword')

        # Проверка, существует ли уже такой проект
        existing_project = Client.query.filter_by(name=project_name).first()
        if existing_project:
            return {'status': 'warning', 'text': f'{project_name} уже существует. Имя должно быть уникальным.'}

        try:
            # Если проекта не существует, продолжаем добавление
            project_password_hash = bcrypt.generate_password_hash(project_password).decode('utf-8')
            project_date = request.form.get('projectDate').replace('.', '-')
            date_object = datetime.strptime(project_date, '%d-%m-%Y')

            new_project = Client(name=project_name, password=project_password_hash, date=date_object)
            db.session.add(new_project)
            db.session.commit()

            return {'status': 'success', 'text': f'Проект с именем {project_name} создан.'}
        except Exception as e:
            return {'status': 'error', 'text': f'{e}'}


def change_project_password(app):
    with app.app_context():
        project_name = request.form.get('projectName')
        project_password = request.form.get('projectPassword')

        existing_project = Client.query.filter_by(name=project_name).first()
        if existing_project:
            project_password_hash = bcrypt.generate_password_hash(project_password).decode('utf-8')

            existing_project.password = project_password_hash

            db.session.commit()

            return {'status': 'success', 'text': f'Пароль для {project_name} изменен.'}
        else:
            return {'status': 'info', 'text': 'Проекта не существует, обратитесь к администратору.'}
