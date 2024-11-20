import os
from PIL import Image
from Path import PortfolioDir
from random import choice


def get_html_for_portfolio(portfolio, alt_tags):
    portfolio_dir = PortfolioDir(portfolio)
    index = 0
    gallery_file_path = os.path.join(portfolio_dir.main_path, 'gallery.html')

    if os.path.exists(gallery_file_path):
        with open(gallery_file_path, 'r', encoding='utf-8') as file:
            gallery_html = file.read()
    else:
        # Создание содержимого gallery_html
        images = [f for f in os.listdir(portfolio_dir.blur_path) if
                  os.path.isfile(os.path.join(portfolio_dir.blur_path, f))]
        gallery_html = ''

        for img_name in images:
            file_name, _ = os.path.splitext(img_name)
            img_path = os.path.join(portfolio_dir.small_path, img_name)
            pswp_img_path = os.path.join(portfolio_dir.main_path, img_name)

            with Image.open(img_path) as img:
                width, height = img.size
                ratio = width / height
                style = ''

            with Image.open(pswp_img_path) as img:
                width_pswp, height_pswp = img.size

            gallery_html += f'''
                            <div class="grid-item item" data-filename="{file_name}" style="ratio: {ratio}; {style}">
                                <a href="/static/media/{portfolio}/{file_name}.webp" data-pswp-width="{width_pswp}" data-pswp-height="{height_pswp}" data-pswp data-caption="Anfangsjahr">
                                    <img src="/static/media/{portfolio}/blur/{file_name}.webp"
                                        data-src="/static/media/{portfolio}/small/{file_name}.webp"
                                        alt="{alt_tags[index]}" width="{width}" height="{height}" loading='lazy'
                                        _="on intersection(intersecting) having threshold 0.25 if intersecting transition opacity to 1">
                                </a>
                            </div>
                        '''
            index += 1
        with open(gallery_file_path, 'w', encoding='utf-8') as file:
            file.write(gallery_html)

    return gallery_html


def clear_portfolio_html():
    portfolio = ['newborn', 'babybauch', 'baby']
    for item in portfolio:
        portfolio_dir = PortfolioDir(item)
        gallery_file_path = os.path.join(portfolio_dir.main_path, 'gallery.html')
        if os.path.exists(gallery_file_path):
            os.remove(gallery_file_path)
            print('Gelöscht')


def key_number(key = None):
    numbers = {'0zBI8jGMli': '10', 'BR1lkp1Jcy': '11', 'DUerZ2bMzC': '12', 'llgSzjK4Qm': '13', 'x9KtQsOAPG': '14',
               'OQ9tlwoFuG': '15', 'koSFn0J1Ae': '16', 'VuOpfwUF4u': '17', '9PF01a1GC.': '18', 'wyG3VE5jEm': '19',
               'gJsIFEmRqe': '20'}
    if key:
        return numbers[key]

    return choice(list(numbers.keys()))
