import os
import zipfile

from flask import request

from Models import UserDirectories, Client, db, Project


class ProjectProof(Project):
    __name__ = 'ProjectProof'
    __annotations__ = '''Наследование от Project (где инициализация по Username)'''

    def main_pic(self):
        for item in os.listdir(UserDirectories(self.username).main_path):
            if os.path.isfile(os.path.join('static', 'media', 'clients', self.username, item)):
                return item

    def approved_images(self, app):
        with app.app_context():
            project = Client.query.filter_by(name=self.username).first()
        return project.fotos_list.split(', ') if project.fotos_list else []

    def add_image_to_db(self, app):
        """Add photo's name to db as approved photo"""

        with app.app_context():
            project = Client.query.filter_by(name=self.username).first()

            filename = request.get_json().get('fileName')
            if not project:
                return 'error'
            if project.fotos_list:
                photos = project.fotos_list.split(', ')
                if filename not in photos:
                    project.fotos_list += f", {filename}"
                else:
                    return 'foto exists'
            else:
                project.fotos_list = filename
            db.session.commit()
        return 'success'


    def remove_image_from_db(self, app):
        with app.app_context():
            project = Client.query.filter_by(name=self.username).first()
            filename = request.get_json().get('fileName')

            if not project:
                return 'error'
            if project.fotos_list:
                fotos = project.fotos_list.split(', ')
                if filename in fotos:
                    fotos.remove(filename)
                    project.fotos_list = ', '.join(fotos)
                else:
                    return 'foto not exists'
            else:
                project.fotos_list = filename

            db.session.commit()
        return 'success'


    def download_client_gallery(self):
        # Определяем путь к пользовательской директории
        user_dir = UserDirectories(self.username).main_path
        download_dir = os.path.join(user_dir, 'download')

        os.makedirs(download_dir, exist_ok=True)

        # Путь к файлу zip в пользовательской директории
        zip_file_path = os.path.join(user_dir, 'download', 'download.zip')

        if (os.path.exists(zip_file_path) and os.path.getsize(zip_file_path) > 0):
            return zip_file_path

        # Создаем zip-файл в пользовательской директории
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file in os.listdir(user_dir):
                file_path = os.path.join(user_dir, file)  # Полный путь к файлу
                if os.path.isfile(file_path):
                    zipf.write(file_path, file)  # Добавляем файл в zip с относительным путем

        # Возвращаем путь к zip-файлу
        return zip_file_path
