import datetime

from flask import request, Response, render_template
from flask_login import UserMixin

from Models import db, bcrypt
from Path import UserDirectories


class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, unique=True)
    # fotos_list = db.Column(db.Text, nullable=True)
    fotos_list = db.Column(db.JSON, nullable=True, default=list)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, password, date):
        self.name = name
        self.password = password
        self.date = date

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'fotos_list': self.fotos_list,
            'date': self.date.isoformat() if self.date else None
        }

    def clear_foto_list(self, app):
        with app.app_context():
            try:
                self.fotos_list = []
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


class GetClient:
    __slots__ = ("__app",)

    def __init__(self, app):
        self.__app = app

    def filter_by(self, id: int = None, name: str = None) -> Client | None:
        if id is None and name is None:
            raise ValueError("Необходимо указать либо id, либо name для фильтрации клиента.")

        with self.__app.app_context():
            if id is not None:
                return Client.query.filter_by(id=id).first()
            elif name is not None:
                return Client.query.filter_by(name=name).first()
            else:
                return None


class ProjectManager:
    __slots__ = ("__app",)

    def __init__(self, app):
        self.__app = app

    def add_new(self, project_name: str) -> dict:
        with self.__app.app_context():
            # Проверка, существует ли уже такой проект
            existing_project = GetClient.filter_by(self.__app, name=project_name)
            if existing_project is not None:
                return {'status': 'warning', 'text': f'{project_name} уже существует. Имя должно быть уникальным.'}

            try:
                # Если проекта не существует, продолжаем добавление
                project_password = request.form.get('projectPassword')  # Get password from request form
                project_password_hash = bcrypt.generate_password_hash(project_password).decode('utf-8')

                project_date = request.form.get('projectDate').replace('.', '-')  # Get date from request form
                date_object = datetime.datetime.strptime(project_date, '%d-%m-%Y')

                new_project = Client(name=project_name, password=project_password_hash, date=date_object)

                db.session.add(new_project)
                db.session.commit()

                UserDirectories(new_project.name).create_paths()

                return {'status': 'success', 'text': f'Проект с именем {project_name} создан.'}
            except Exception as e:
                return {'status': 'error', 'text': f'{e}'}

    def delete(self, project: str) -> Response:
        with self.__app.app_context():
            try:
                db.session.delete(project)
                db.session.commit()

                if UserDirectories(project.name).delete_project_path() == False:
                    response = Response(render_template('/hilfsportal/alert.html', status='warning',
                                                        text=f"Невозможно удалить содержимое проекта {project.name}. Обратитесь к администратору."))
                    response.headers['X-Success'] = 'warning'
                    return response

                response = Response(render_template('/hilfsportal/alert.html', status='success',
                                                    text=f"Проект {project.name} был удален."))
                response.headers['X-Success'] = 'success'
            except Exception as e:
                response = Response(render_template('/hilfsportal/alert.html', status='warning', text=f"{e}"))
                response.headers['X-Success'] = 'warning'
            return response

    def change_password(self, name: str, psw: str) -> dict:
        with self.__app.app_context():
            existing_project = GetClient.filter_by(self.__app, name=name)

            if existing_project is not None:
                project_password_hash = bcrypt.generate_password_hash(psw).decode('utf-8')
                existing_project.password = project_password_hash

                db.session.commit()
                return {'status': 'success', 'text': f'Пароль для {name} изменен.'}

            else:
                return {'status': 'info', 'text': 'Проекта не существует, обратитесь к администратору.'}
