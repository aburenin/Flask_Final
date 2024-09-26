import os
import zipfile
import time

from flask import request
from pickle import APPENDS
from token import NEWLINE

from Models import UserDirectories, Client, db


def check_main_picture(username):
    for item in os.listdir(UserDirectories(username).main_path):
        if os.path.isfile(os.path.join('static', 'media', 'clients', username, item)):
            return item


def get_client_main_pictures(username):
    user = UserDirectories(username)
    folder_path = [user.blur_path, user.small_path]
    pictures = []
    for path in folder_path:
        files = os.listdir(path)
        if files:
            pictures.append(os.path.join(path, files[0]).replace('\\', '/'))
        else:
            return []  # Если в папке нет изображений
    return pictures


def check_approved_imges(app, username):
    with app.app_context():
        project = Client.query.filter_by(name=username).first()        
        if project.fotos_list:
            fotos = project.fotos_list.split(', ')
            return fotos
        else:
            return []


def add_image_to_db(app, username):
    with app.app_context():
        project = Client.query.filter_by(name=username).first()
        filename = request.get_json().get('fileName')
        if not project:
            return 'error'
        if project.fotos_list:
            fotos = project.fotos_list.split(', ')
            if filename not in fotos:
                project.fotos_list += f", {filename}"
            else:
                return 'foto exists'
        else:
            project.fotos_list = filename

        db.session.commit()
        return 'success'


def remove_image_from_db(app, username):
    with app.app_context():
        project = Client.query.filter_by(name=username).first()
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

def download_client_gallery(username):
    # Определяем путь к пользовательской директории
    user_dir = UserDirectories(username).main_path
    download_dir = os.path.join(user_dir, 'download')

    os.makedirs(download_dir, exist_ok=True)

    # Путь к файлу zip в пользовательской директории
    zip_file_path = os.path.join(user_dir, 'download','download.zip')

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