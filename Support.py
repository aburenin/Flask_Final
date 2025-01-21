from PIL import Image, ExifTags
from flask import request, jsonify
from random import choice
from flask_mail import Mail, Message
import os
import requests

from config import SECRET_KEY


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


class EmailSender:

    __slots__ = ('__mail', '__msg', '__app')

    def __init__(self, app):
        self.__mail = Mail(app)
        self.__msg = Message(subject=request.form.get('inputGroupSelect01'),
                          sender=('Fotografie Baby Babybauch & Kinder', 'info@fotos-baby.de'),
                          recipients=['burenin.alexey@gmail.com'])
        self.__app = app


    def send(self, app):
        with app.app_context():
            msg_body = (f'Von: {request.form.get('firstName')} '
                        f'{request.form.get('lastName')}\n'
                        f'Tel.: {request.form.get('phone')}\n'
                        f'E-mail: {request.form.get('email')}\n'
                        f'Betreff: {request.form.get('inputGroupSelect01')}\n\n'
                        f'Message:\n{request.form.get('message')}'
                        "\n\n--------------------\nDiese E-Mail wurde von einem Kontaktformular von "
                        "Baby, Babybauch & Kinder Fotografie (https://fotos-baby.ch) gesendet.")

            self.__msg.body = msg_body

            self.__mail.send(self.__msg)


# class EmailSender:
#
#     __slots__ = ('__mail', '__msg', '__app')
#
#     def __init__(self, app):
#         self.__mail = Mail(app)
#         self.__msg = Message(subject=request.form.get('inputGroupSelect01'),
#                           sender=('Fotografie Baby Babybauch & Kinder', 'info@fotos-baby.de'),
#                           recipients=['burenin.alexey@gmail.com'])
#         self.__app = app
#
#
#     def send(self):
#         with self.__app.app_context():
#             msg_body = (f'Von: {request.form.get('firstName')} '
#                         f'{request.form.get('lastName')}\n'
#                         f'Tel.: {request.form.get('phone')}\n'
#                         f'E-mail: {request.form.get('email')}\n'
#                         f'Betreff: {request.form.get('inputGroupSelect01')}\n\n'
#                         f'Message:\n{request.form.get('message')}'
#                         "\n\n--------------------\nDiese E-Mail wurde von einem Kontaktformular von "
#                         "Baby, Babybauch & Kinder Fotografie (https://fotos-baby.ch) gesendet.")
#
#             self.__msg.body = msg_body
#
#             self.__mail.send(self.__msg)
