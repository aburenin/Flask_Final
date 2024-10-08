import os

from PIL import Image
from bs4 import BeautifulSoup, Tag
from requests import request

from Models import PortfolioDir


def get_html_for_portfolio(portfolio, alt_tags):
    portfolio_dir = PortfolioDir(portfolio)
    index = 0
    gallery_file_path = os.path.join(portfolio_dir.portfolio_main, 'gallery.html')

    if os.path.exists(gallery_file_path):
        with open(gallery_file_path, 'r', encoding='utf-8') as file:
            gallery_html = file.read()
    else:
        # Создание содержимого gallery_html
        images = [f for f in os.listdir(portfolio_dir.portfolio_blur) if
                  os.path.isfile(os.path.join(portfolio_dir.portfolio_blur, f))]
        gallery_html = ''

        for img_name in images:
            file_name, _ = os.path.splitext(img_name)
            img_path = os.path.join(portfolio_dir.portfolio_small, img_name)
            pswp_img_path = os.path.join(portfolio_dir.portfolio_main, img_name)

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
        gallery_file_path = os.path.join(portfolio_dir.portfolio_main, 'gallery.html')
        if os.path.exists(gallery_file_path):
            os.remove(gallery_file_path)
            print('Gelöscht')


# ======================================================================================================================
# 👉👉👉                       ▶️▶️▶️ Datenschutz from It-Recht-Kanzlei  ◀️◀️◀️                                 👈👈👈
# ================================================🔽🔽🔽🔽🔽🔽=========================================================
def parser_datenschutz():
    response = request(url='https://itrk.legal/jrV.8V.eA2.html', method='get')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        h1_tag = soup.find('h1')
        footer_tag = soup.find('footer')

        if h1_tag and footer_tag:
            elements_between = []

            for elem in h1_tag.find_next_siblings():
                if elem == footer_tag:
                    break
                if isinstance(elem, Tag):  # Пропустить текстовые узлы (NavigableString)
                    elements_between.append(str(elem))

            result = "\n".join(elements_between)
            return (result)

    else:
        return (f"Failed to get the webpage: HTTP {response.status_code}. Please contact us per info@fotos-baby.de")
