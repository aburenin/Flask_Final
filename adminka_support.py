import os
import threading

from PIL import Image, ImageFilter
from flask import copy_current_request_context
from flask import jsonify, request

from Path import UserDirectories

from Client import Client
from Proof import ProjectProof


def get_client_data():
    index = int(request.args.get('lastindex'))
    clients = Client.query.offset(index).limit(10).all()
    clients_data = []
    for client in clients:
        client_dict = client.to_dict()
        # Используем функцию для получения URL изображения
        client_dict['img_url'] = UserDirectories(client.name).get_client_image_url()
        client_dict['path_size'] = UserDirectories(client.name).count_files_and_size()
        clients_data.append(client_dict)
    return jsonify(clients_data)


def upload_files(uploaded_file, projectName):
    if projectName:
        user = UserDirectories(projectName)

    if uploaded_file and allow_extension(filename=uploaded_file.filename):
        # Сохраняем файл в папку пользователя.
        file_path = os.path.join(user.main_path, uploaded_file.filename)
        uploaded_file.save(file_path)

        @copy_current_request_context
        def process_image():
            img = Image.open(file_path)  # Здесь следует открывать файл по пути, а не объект uploaded_file
            img = ProjectProof.correct_image_orientation(img)

            # Уменьшите изображение
            img.thumbnail((600, 900), Image.LANCZOS)
            img.save(os.path.join(user.small_path, uploaded_file.filename.split('.')[0] + '.webp'), 'WebP', quality=95)

            # Blurim изображение
            img.thumbnail((300, 300), Image.LANCZOS)
            # img.thumbnail((225, 175), Image.LANCZOS)
            # img.thumbnail((705, 1100), Image.LANCZOS)
            blurred = img.filter(ImageFilter.GaussianBlur(6))
            blurred.save(os.path.join(user.blur_path, uploaded_file.filename.split('.')[0] + '.webp'), 'WebP')

        # Запуск обработки изображения в отдельном потоке
        thread = threading.Thread(target=process_image)
        thread.start()

        return {'status': 'success', 'message': f'File {uploaded_file.filename} uploaded successfully'}

    return {'status': 'failure', 'message': 'No file uploaded'}


def allow_extension(filename):
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    return os.path.splitext(filename)[1].lower() in allowed_extensions



