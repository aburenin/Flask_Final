from PIL import Image, ExifTags
from flask import request, jsonify
from random import choice

class ImageOrientation:
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





class Recaptcha:
    NUMBERS = {
        '0zBI8jGMli': '10', 'BR1lkp1Jcy': '11', 'DUerZ2bMzC': '12', 'llgSzjK4Qm': '13', 'x9KtQsOAPG': '14',
        'OQ9tlwoFuG': '15', 'koSFn0J1Ae': '16', 'VuOpfwUF4u': '17', '9PF01a1GC.': '18', 'wyG3VE5jEm': '19',
        'gJsIFEmRqe': '20'
    }

    @classmethod
    def get(cls):
        """Возвращает случайный ключ из NUMBERS."""
        return choice(list(cls.NUMBERS.keys()))

    @classmethod
    def check(cls, key):
        """Проверяет, есть ли ключ в NUMBERS, и возвращает значение или None."""
        return cls.NUMBERS[key]
        # token = request.form.get('token')
        # key = request.form.get('key')
        # return (jsonify({"status": "success"}), 200) if cls.NUMBERS.get(key) == token else (jsonify({"status": "failure"}), 400)

