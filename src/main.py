from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from requests_cache import CachedSession

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR, MAIN_DOC_URL, PEP_MAIN_URL, EXPECTED_STATUS
)
from outputs import control_output
from utils import get_response, find_tag


def whats_new(session):
    result = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    soup = BeautifulSoup(
        get_response(session, urljoin(MAIN_DOC_URL, 'whatsnew/')).text,
        features='lxml'
    )
    tags = soup.find_all(class_='toctree-l1')
    for tag in tags:
        version_link = urljoin(
                urljoin(MAIN_DOC_URL, 'whatsnew/'),
                tag.find('a')['href']
            )
        soup = BeautifulSoup(get_response(session, version_link).text,
                             features='lxml')
        result.append((version_link,
                      find_tag(soup, 'h1').text,
                      find_tag(soup, 'dl').text.replace('\n', ' ').strip()))
    return result


def latest_versions(session):
    result = [('Ссылка на документацию', 'Версия', 'Статус')]
    return result


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = BeautifulSoup(
        get_response(session, downloads_url).text, features='lxml'
    )
    table_download = soup.find(class_='docutils')
    pdf_a4_tag = table_download.find(
        'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = get_response(session, archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)


def pep(session):
    pass


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    session = CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results:
        control_output(results, args)


if __name__ == '__main__':
    main()
