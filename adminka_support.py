import os
import shutil
import threading
from importlib.metadata import files

from PIL import Image, ImageFilter, ExifTags
from flask import copy_current_request_context, url_for
from flask import jsonify, request, render_template, Response

from Models import Client, UserDirectories, db


def get_client_data():
    index = int(request.args.get('lastindex'))
    clients = Client.query.offset(index).limit(10).all()
    clients_data = []
    for client in clients:
        client_dict = client.to_dict()
        # Используем функцию для получения URL изображения
        client_dict['img_url'] = get_client_image_url(client.name)
        client_dict['path_size'] = count_files_and_size(client.name)
        clients_data.append(client_dict)
    return jsonify(clients_data)


# Функция возвращает путь к фотке для представления клиентских проектов
def get_client_image_url(client_name):
    base_path = os.path.join('static', 'media', 'clients')
    default_img = url_for('static', filename='img/back_client.svg')  # URL по умолчанию
    client_folder = os.path.join(base_path, client_name, 'small')

    if os.path.isdir(client_folder):
        # Получаем список всех файлов в папке
        files = [f for f in os.listdir(client_folder) if os.path.isfile(os.path.join(client_folder, f))]
        # Фильтруем файлы, оставляя только изображения
        images = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        if images:
            # Формируем корректный URL с прямыми косыми чертами
            image_url = os.path.join('media', 'clients', client_name, 'small', images[0]).replace('\\', '/')
            return url_for('static', filename=image_url)

    # Возвращаем изображение по умолчанию, если папка не существует или в ней нет изображений
    return default_img


# Функция возвращает размер клиентских проектов
def count_files_and_size(client_name):
    client_folder = os.path.join('static', 'media', 'clients', client_name)
    file_count = 0
    total_size = 0

    if os.path.exists(client_folder):
        for item in os.listdir(client_folder):
            item_path = os.path.join(client_folder, item)
            if os.path.isfile(item_path):
                file_count += 1
                total_size += os.path.getsize(item_path)

    total_size_mb = round(total_size / (1024 ** 2), 2)
    if total_size_mb > 0:
        return f'{file_count} files, {total_size_mb} Mb'
    else:
        return 'Пусто'


def create_paths(username) -> bool:
    paths = UserDirectories(username).get_paths()
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)
    return True


def delete_project_path(username) -> bool:
    paths = UserDirectories(username).get_paths()
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)  # Удаляем директорию и все её содержимое
            return True
        else:
            return False


def upload_files(uploaded_file, projectName):
    user = UserDirectories(projectName)

    if uploaded_file and allow_extension(filename=uploaded_file.filename):
        # Сохраняем файл в папку пользователя.
        file_path = os.path.join(user.main_path, uploaded_file.filename)
        uploaded_file.save(file_path)

        # socketio.emit('log', {'action': 'start', 'filename': uploaded_file.filename})

        @copy_current_request_context
        def process_image():
            img = Image.open(file_path)  # Здесь следует открывать файл по пути, а не объект uploaded_file
            img = correct_image_orientation(img)
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


def clear_client_gallery(projectName: str):
    user = UserDirectories(projectName)

    if os.path.exists(user.main_path):
        # Clearing all contents of the folder
        for filename in os.listdir(user.main_path):
            file_path = os.path.join(user.main_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    os.makedirs(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
                return {'status': 'error', 'message': f'{e}'}
        return {'status': 'success', 'message': 'Все фото были удалены.'}
    else:
        return {'status': 'warning', 'message': f'Данной папки не существует, обратитесь к администратору.'}


def delete_img_from_gallery(projectName: str, fileName: str):
    #----  return никак не обрабатывается сейячас ....
    user = UserDirectories(projectName)

    if os.path.exists(user.main_path):
        # Перебираем все подпапки
        for root, dirs, files in os.walk(user.main_path):
            for file in files:
                # Получаем имя файла без расширения
                name, ext = os.path.splitext(file)
                # Сравниваем с переданным именем файла
                if name == fileName:
                    file_path = os.path.join(root, file)
                    try:
                        os.unlink(file_path)  # Удаление файла
                        print(f'{file_path} удален.')
                    except Exception as e:
                        print(f'Не удалось удалить {file_path}. Причина: {e}')
                        return {'status': 'error', 'message': f'{e}'}
        return {'status': 'success', 'message': f'Файл {fileName} был удален из всех папок.'}
    else:
        return {'status': 'warning', 'message': 'Данной папки не существует, обратитесь к администратору.'}


def allow_extension(filename):
    _, file_extension = os.path.splitext(filename)
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.png'}
    if file_extension.lower() not in allowed_extensions:
        return False
    else:
        return True


def correct_image_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = image._getexif()
        if exif is not None:
            orientation = exif.get(orientation, None)

            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except Exception as e:
        print(f"Error correcting image orientation: {e}")

    return image


def get_html_for_gallery(projectName):
    user = UserDirectories(projectName)
    index = 0

    images = [f for f in os.listdir(user.main_path) if os.path.isfile(os.path.join(user.main_path, f))]
    images.sort()
    gallery_html = ''

    for img_name in images:
        file_name, type = os.path.splitext(img_name)
        img_path = os.path.join(user.small_path, file_name + '.webp')
        pswp_img_path = os.path.join(user.main_path, img_name)

        with Image.open(img_path) as img:
            img = correct_image_orientation(img)
            width, height = img.size
            ratio = width / height
            style = ''

        with Image.open(pswp_img_path) as img:
            img = correct_image_orientation(img)
            width_pswp, height_pswp = img.size

        gallery_html += f'''
                            <div class="grid-item item" data-filename="{file_name}" style="ratio: {ratio}; {style}">
                                <div class="del-img"></div>
                                <a href="/static/media/clients/{projectName}/{file_name}{type}" data-pswp-width="{width_pswp}" data-pswp-height="{height_pswp}" data-pswp data-caption="Anfangsjahr">
                                    <span>{file_name}</span>
                                    <img src="/static/media/clients/{projectName}/blur/{file_name}.webp"
                                        data-src="/static/media/clients/{projectName}/small/{file_name}.webp"
                                        alt="{img_name}" width="{width}" height="{height}" loading='lazy'
                                        _="on intersection(intersecting) having threshold 0.25 if intersecting transition opacity to 1">
                                </a>
                                <div class="proofing--footer">
                                    <button class="btn heart--selection" _="on click toggle .selected on me"></button>
                                </div>
                            </div>
                        '''
        index += 1

    return gallery_html


def delete_project(app, id):
    with app.app_context():
        try:
            project = Client.query.filter_by(id=id).first()

            db.session.delete(project)
            db.session.commit()

            if delete_project_path(project.name) == False:
                response = Response(render_template('/hilfsportal/alert.html', status='warning',
                                                    text=f"Невозможно удалить содержимое рроекта {project.name}. Обратитесь к администратору."))
                response.headers['X-Success'] = 'warning'
                return response

            response = Response(
                render_template('/hilfsportal/alert.html', status='success', text=f"Проект {project.name} был удален."))
            response.headers['X-Success'] = 'success'
        except Exception as e:
            response = Response(render_template('/hilfsportal/alert.html', status='warning', text=f"{e}"))
            response.headers['X-Success'] = 'warning'
        return response
    
    
def clear_foto_list(app, id):
    with app.app_context():
        try:
            project = Client.query.filter_by(id=id).first()

            project.fotos_list = ''
            db.session.commit()

            response = Response(
                render_template('/hilfsportal/alert.html', status='success', text=f"Проект {project.name} был очищен."))
            response.headers['X-Success'] = 'success'
        except Exception as e:
            response = Response(render_template('/hilfsportal/alert.html', status='warning', text=f"{e}"))
            response.headers['X-Success'] = 'warning'
        return response