import os
from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash

from Models import db, Preise, Question, Client, bcrypt
from config import qa_list, pakets

from flask import jsonify, request, Flask


def check_db_instance(app):
    if not os.path.exists('instance/fotos-baby.db'):
        with app.app_context():
            db.create_all()
    create_preise_table(app)
    create_question_table(app)

def create_preise_table(app):
    # Список с данными для добавления pakets
    with app.app_context():
        # Проходимся по списку пакетов
        for name, price, description in pakets:
            # Ищем существующий пакет с таким же именем
            existing_paket = Preise.query.filter_by(name=name).first()

            if existing_paket:
                # Флаг для отслеживания изменений
                changes = False
                # Сравниваем цены, если есть изменения, обновляем значение и устанавливаем флаг
                if existing_paket.price != price:
                    existing_paket.price = price
                    changes = True
                # Сравниваем описания, если есть изменения, обновляем значение и устанавливаем флаг
                if existing_paket.description != description:
                    existing_paket.description = description
                    changes = True

                # Если были изменения, делаем commit
                if changes:
                    db.session.commit()
            else:
                # Если пакет не найден, создаем новый и добавляем его в базу данных
                paket = Preise(name=name, price=price, description=description)
                try:
                    db.session.add(paket)
                    db.session.commit()
                except:
                    db.session.rollback()


def create_question_table(app):
    # Список с данными для добавления pakets

    with app.app_context():
        # Проходимся по списку пакетов
        for question, answer in qa_list:
            # Ищем существующий пакет с таким же именем
            existing_qa = Question.query.filter_by(question=question).first()

            if existing_qa:
                # Флаг для отслеживания изменений
                changes = False
                # Сравниваем цены, если есть изменения, обновляем значение и устанавливаем флаг
                if existing_qa.question != question:
                    existing_qa.question = question
                    changes = True
                # Сравниваем описания, если есть изменения, обновляем значение и устанавливаем флаг
                if existing_qa.answer != answer:
                    existing_qa.answer = answer
                    changes = True

                # Если были изменения, делаем commit
                if changes:
                    db.session.commit()
            else:
                # Если пакет не найден, создаем новый и добавляем его в базу данных
                paket = Question(question=question, answer=answer)
                try:
                    db.session.add(paket)
                    db.session.commit()
                except:
                    db.session.rollback()


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