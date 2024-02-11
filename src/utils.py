from bs4 import BeautifulSoup
from exceptions import ParserFindTagException


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if not searched_tag:
        raise ParserFindTagException(f'Не найден тег {tag} {attrs}')
    return searched_tag


def get_response(session, url, encoding='utf-8'):
    response = session.get(url)
    response.encoding = encoding
    return response


def get_soup(session, url, parser='lxml'):
    return BeautifulSoup(get_response(session, url).text, parser)
