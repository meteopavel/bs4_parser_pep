from bs4 import BeautifulSoup
import logging
import re
from urllib.parse import urljoin

from requests_cache import CachedSession
from tqdm import tqdm

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
    for tag in tqdm(tags,
                    total=len(tags),
                    desc='Парсинг в процессе'):
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
    soup = BeautifulSoup(
        get_response(session, MAIN_DOC_URL).text,
        features='lxml'
    )
    tags_ul = soup.find(class_='sphinxsidebarwrapper').find_all('ul')
    for ul in tags_ul:
        if 'All versions' in ul.text:
            tags_a = ul.find_all('a')
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a in tqdm(tags_a,
                  total=len(tags_a),
                  desc='Парсинг в процессе'):
        text_match = re.search(pattern, a.text)
        if text_match:
            version, status = text_match.groups()
        else:
            version, status = a.text, ''
        result.append(
            (a['href'], version, status)
        )
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
    soup = BeautifulSoup(
        get_response(session, PEP_MAIN_URL).text,
        features='lxml'
    )
    relative_pep_urls = []
    table_links = soup.find_all(class_='pep-zero-table docutils align-default')
    inner_table_links = [links.find_all('a') for links in table_links]
    for link in inner_table_links:
        for a in link:
            relative_pep_urls.append(a['href'])
    relative_pep_urls = sorted(set(relative_pep_urls))

    numerical_index_section = soup.find(id='numerical-index')
    abbrs = numerical_index_section.find_all('abbr')
    table_statuses = [abbr.text[1:] for abbr in abbrs]

    status_codes = {}
    mismatches = []
    for num, url in tqdm(enumerate(relative_pep_urls),
                         total=len(relative_pep_urls),
                         desc='Парсинг в процессе'):
        soup = BeautifulSoup(
            get_response(session, urljoin(PEP_MAIN_URL, url)).text,
            features='lxml'
        )
        page_status = soup.find('abbr').text
        if page_status not in EXPECTED_STATUS.get(table_statuses[num]):
            mismatches.append(
                'Несовпадение статуса: '
                f'{urljoin(PEP_MAIN_URL, url)} '
                f'Статус на странице: {page_status} '
                f'Статус в списке: {EXPECTED_STATUS.get(table_statuses[num])}'
            )
        if page_status in status_codes:
            status_codes[page_status] += 1
        else:
            status_codes[page_status] = 1
    logging.warning('\n'.join(mismatches))
    return [
        ('Статус', 'Количество'),
        *status_codes.items(),
        ('Итого', str(sum(status_codes.values())))
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Запуск парсера')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    session = CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    result = MODE_TO_FUNCTION[parser_mode](session)
    if result:
        control_output(result, args)
    logging.info('Парсинг завершён')


if __name__ == '__main__':
    main()
