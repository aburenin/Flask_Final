from bs4 import BeautifulSoup, Tag
from requests import request


class Datenschutz:
    """Datenschutz from It-Recht-Kanzlei """
    __slots__ = ("_text",)

    def __init__(self):
        self._text = self.parser(url="https://itrk.legal/jrV.8V.eA2.html")

    @property
    def text(self):
        return self._text

    @staticmethod
    def parser(url: str = "https://itrk.legal/jrV.8V.eA2.html") -> BeautifulSoup:
        response = request(url=url, method='get')
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
                return result

        else:
            return f"Failed to get the webpage: HTTP {response.status_code}. Please contact us per info@fotos-baby.de"
