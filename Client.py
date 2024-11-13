import datetime

from flask_login import UserMixin
from flask import request, Response, render_template

from Models import db, bcrypt

from Path import UserDirectories

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

    @staticmethod
    def get_client_by_id(app, client_id) -> "Client | None":
        with app.app_context():  # создаём контекст приложения
            client = Client.query.filter_by(id=client_id).first()
            return client

    @staticmethod
    def get_client_by_name(app, client_name) -> "Client | None":
        with app.app_context():  # создаём контекст приложения
            client = Client.query.filter_by(name=client_name).first()  # выполняем запрос для поиска клиента
            return client

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

    def clear_foto_list(self, app):
        with app.app_context():
            try:
                self.fotos_list = ''
                db.session.add(self)  # Добавляем объект клиента в сессию
                db.session.commit()

                response = Response(
                    render_template('/hilfsportal/alert.html', status='success',
                                    text=f"Проект {self.name} был очищен."))
                response.headers['X-Success'] = 'success'
            except Exception as e:
                response = Response(render_template('/hilfsportal/alert.html', status='warning', text=f"{e}"))
                response.headers['X-Success'] = 'warning'
            return response

    def delete_project(self, app):
        with app.app_context():

            try:
                db.session.delete(self)
                db.session.commit()

                if UserDirectories(self.name).delete_project_path() == False:
                    response = Response(render_template('/hilfsportal/alert.html', status='warning',
                                                        text=f"Невозможно удалить содержимое проекта {self.name}. Обратитесь к администратору."))
                    response.headers['X-Success'] = 'warning'
                    return response

                response = Response(
                    render_template('/hilfsportal/alert.html', status='success',
                                    text=f"Проект {self.name} был удален."))
                response.headers['X-Success'] = 'success'
            except Exception as e:
                response = Response(render_template('/hilfsportal/alert.html', status='warning', text=f"{e}"))
                response.headers['X-Success'] = 'warning'
            return response