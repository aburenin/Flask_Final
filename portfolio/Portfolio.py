import os

from PIL import Image

from Path import PortfolioDir
from config import alt_tags


class Gallery(PortfolioDir):
    _PORTFOLIO = ['newborn', 'babybauch', 'baby']

    __slots__ = ("_portfolio",)

    def __init__(self, portfolio):
        super().__init__(portfolio)
        self._portfolio = portfolio

    @property
    def portfolio(self):
        return self._portfolio

    def create(self):
        gallery_file_path = os.path.join(self.main_path, 'gallery.html')

        try:
            with open(gallery_file_path, 'r') as file:
                return file.read()
        except (FileNotFoundError, IOError) as e:
            print(e)

        images = [f for f in os.listdir(self.blur_path) if
                  os.path.isfile(os.path.join(self.blur_path, f))]
        gallery_html = []

        for index, img_name in enumerate(images):
            file_name, _ = os.path.splitext(img_name)
            img_path = os.path.join(self.small_path, img_name)
            pswp_img_path = os.path.join(self.main_path, img_name)

            with Image.open(img_path) as img:
                width, height = img.size
                ratio = width / height

            with Image.open(pswp_img_path) as img:
                width_pswp, height_pswp = img.size

            gallery_html.append(f'''<div class="grid-item item" data-filename="{file_name}" style="ratio: {ratio}">
                                <a href="/{self.main_path}/{file_name}.webp" data-pswp-width="{width_pswp}" data-pswp-height="{height_pswp}" data-pswp data-caption="Anfangsjahr">
                                    <img src="/{self.blur_path}/{file_name}.webp"
                                        data-src="/{self.small_path}/{file_name}.webp"
                                        alt="{alt_tags[self.portfolio][index]}" width="{width}" height="{height}" loading='lazy'
                                        _="on intersection(intersecting) having threshold 0.25 if intersecting transition opacity to 1">
                                </a>
                            </div>''')
        try:
            with open(gallery_file_path, 'w+', encoding='utf-8') as file:
                file.writelines(gallery_html)
                print(f"{gallery_file_path} created.")
        except IOError as e:
            print(f"Ошибка при записи файла: {e}")

        return ''.join(gallery_html)

    @classmethod
    def clear_temlates(cls):
        for item in cls._PORTFOLIO:
            gallery_file_path = os.path.join("static", "media", item, 'gallery.html')
            if os.path.exists(gallery_file_path):
                os.remove(gallery_file_path)
            cls(item).create()
