import os
import threading

from PIL import Image, ImageFilter, ExifTags
from flask import copy_current_request_context, url_for
from flask import jsonify, request, render_template, Response

from Models import db
from Path import UserDirectories

from Client import Client


# from support_functions import timer


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
    user = UserDirectories(projectName)

    if uploaded_file and allow_extension(filename=uploaded_file.filename):
        # Сохраняем файл в папку пользователя.
        file_path = os.path.join(user.main_path, uploaded_file.filename)
        uploaded_file.save(file_path)

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


def allow_extension(filename):
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    return os.path.splitext(filename)[1].lower() in allowed_extensions


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
        file_name, _ = os.path.splitext(img_name)
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
                                <a href="/static/media/clients/{projectName}/{img_name}" data-pswp-width="{width_pswp}" data-pswp-height="{height_pswp}" data-pswp data-caption="Anfangsjahr">
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

            if UserDirectories(project.name).delete_project_path() == False:
                response = Response(render_template('/hilfsportal/alert.html', status='warning',
                                                    text=f"Невозможно удалить содержимое проекта {project.name}. Обратитесь к администратору."))
                response.headers['X-Success'] = 'warning'
                return response

            response = Response(
                render_template('/hilfsportal/alert.html', status='success', text=f"Проект {project.name} был удален."))
            response.headers['X-Success'] = 'success'
        except Exception as e:
            response = Response(render_template('/hilfsportal/alert.html', status='warning', text=f"{e}"))
            response.headers['X-Success'] = 'warning'
        return response

