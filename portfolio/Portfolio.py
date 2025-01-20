import os
from PIL import Image
from Path import Path, PortfolioDir

class Gallery(Path):
    _PORTFOLIO = ['newborn', 'babybauch', 'baby']

    @staticmethod
    def create(portfolio, alt_tags):
        portfolio_dir = PortfolioDir(portfolio)
        gallery_file_path = os.path.join(portfolio_dir.main_path, 'gallery.html')

        if os.path.exists(gallery_file_path):
            with open(gallery_file_path, 'r', encoding='utf-8') as file:
                gallery_html = file.read()
        else:
            # Создание содержимого gallery_html
            images = [f for f in os.listdir(portfolio_dir.blur_path) if
                      os.path.isfile(os.path.join(portfolio_dir.blur_path, f))]
            gallery_html = []

            for index, img_name in enumerate(images):
                file_name, _ = os.path.splitext(img_name)
                img_path = os.path.join(portfolio_dir.small_path, img_name)
                pswp_img_path = os.path.join(portfolio_dir.main_path, img_name)

                with Image.open(img_path) as img:
                    width, height = img.size
                    ratio = width / height

                with Image.open(pswp_img_path) as img:
                    width_pswp, height_pswp = img.size

                gallery_html.append(f'''<div class="grid-item item" data-filename="{file_name}" style="ratio: {ratio}">
                                    <a href="/static/media/{portfolio}/{file_name}.webp" data-pswp-width="{width_pswp}" data-pswp-height="{height_pswp}" data-pswp data-caption="Anfangsjahr">
                                        <img src="/static/media/{portfolio}/blur/{file_name}.webp"
                                            data-src="/static/media/{portfolio}/small/{file_name}.webp"
                                            alt="{alt_tags[index]}" width="{width}" height="{height}" loading='lazy'
                                            _="on intersection(intersecting) having threshold 0.25 if intersecting transition opacity to 1">
                                    </a>
                                </div>''')
            try:
                with open(gallery_file_path, 'w+', encoding='utf-8') as file:
                    file.writelines(gallery_html)
            except IOError as e:
                print(f"Ошибка при записи файла: {e}")


        return ''.join(gallery_html)

    @classmethod
    def clear(cls):
        # portfolio = ['newborn', 'babybauch', 'baby']
        for item in cls._PORTFOLIO:
            portfolio_dir = PortfolioDir(item)
            gallery_file_path = os.path.join(portfolio_dir.main_path, 'gallery.html')
            if os.path.exists(gallery_file_path):
                os.remove(gallery_file_path)
                print('Gelöscht')