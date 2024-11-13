import os
import zipfile

from flask import request

from PIL import Image, ImageFilter, ExifTags
from sqlalchemy.dialects.postgresql import array

from Models import db
from Path import UserDirectories
from Client import Client

from typing import Optional

class ProjectProof:
    __name__ = 'ProjectProof'
    """Наследование от Project (где инициализация по Username)"""

    def __init__(self, username):
        self.username = username

    def main_pic(self) -> Optional[str]:
        for item in os.listdir(UserDirectories(self.username).main_path):
            if os.path.isfile(os.path.join('static', 'media', 'clients', self.username, item)):
                return item

    def approved_images(self, app) -> list[str]:
        """Return approved photos list from DB"""
        with app.app_context():
            project = Client.query.filter_by(name=self.username).first()
        return project.fotos_list.split(', ') if project.fotos_list else []

    def add_image_to_db(self, app) -> str:
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

    def remove_image_from_db(self, app) -> str:
        """Add photo's name from db client."""
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

    def download_client_gallery(self) -> Optional[str]:
        """Make ZIP with client photos from gallery"""
        # Определяем путь к пользовательской директории
        user_dir = UserDirectories(self.username).main_path
        download_dir = os.path.join(user_dir, 'download')

        os.makedirs(download_dir, exist_ok=True)

        # Путь к файлу zip в пользовательской директории
        zip_file_path = os.path.join(user_dir, 'download', 'download.zip')

        if os.path.exists(zip_file_path) and os.path.getsize(zip_file_path) > 0:
            return zip_file_path

        # Создаем zip-файл в пользовательской директории
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file in os.listdir(user_dir):
                file_path = os.path.join(user_dir, file)  # Полный путь к файлу
                if os.path.isfile(file_path):
                    zipf.write(file_path, file)  # Добавляем файл в zip с относительным путем

        # Возвращаем путь к zip-файлу
        return zip_file_path


    def get_html_for_gallery(self) -> str:
        user = UserDirectories(self.username)
        index = 0

        images = [f for f in os.listdir(user.main_path) if os.path.isfile(os.path.join(user.main_path, f))]
        images.sort()
        gallery_html = ''

        for img_name in images:
            file_name, _ = os.path.splitext(img_name)
            img_path = os.path.join(user.small_path, file_name + '.webp')
            pswp_img_path = os.path.join(user.main_path, img_name)

            with Image.open(img_path) as img:
                img = ProjectProof.correct_image_orientation(img)
                width, height = img.size
                ratio = width / height
                style = ''

            with Image.open(pswp_img_path) as img:
                img = ProjectProof.correct_image_orientation(img)
                width_pswp, height_pswp = img.size

            gallery_html += f'''
                                <div class="grid-item item" data-filename="{file_name}" style="ratio: {ratio}; {style}">
                                    <div class="del-img"></div>
                                    <a href="/static/media/clients/{self.username}/{img_name}" data-pswp-width="{width_pswp}" data-pswp-height="{height_pswp}" data-pswp data-caption="Anfangsjahr">
                                        <span>{file_name}</span>
                                        <img src="/static/media/clients/{self.username}/blur/{file_name}.webp"
                                            data-src="/static/media/clients/{self.username}/small/{file_name}.webp"
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

    @staticmethod
    def correct_image_orientation(image: Image.Image) -> Image.Image:
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

