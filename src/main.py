import logging
import re
import requests
from collections import defaultdict
from urllib.parse import urljoin

from requests_cache import CachedSession
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR, DirConstants, LiteralConstants, UrlConstants
)
from outputs import control_output
from utils import find_tag, get_response, get_soup


def whats_new(session):
    logger_stack = []
    result = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    soup = get_soup(session, urljoin(UrlConstants.MAIN_DOC_URL, 'whatsnew/'))
    tags = soup.find_all(class_='toctree-l1')
    for tag in tqdm(tags,
                    total=len(tags),
                    desc=LiteralConstants.PARSER_PROCESS):
        version_link = urljoin(
                urljoin(UrlConstants.MAIN_DOC_URL, 'whatsnew/'),
                tag.find('a')['href']
            )
        try:
            soup = get_soup(session, version_link)
            result.append(
                (version_link,
                 find_tag(soup, 'h1').text,
                 find_tag(soup, 'dl').text.replace('\n', ' ').strip())
            )
        except requests.RequestException as error:
            logger_stack.append(error)
    [logging.error(exception) for exception in logger_stack]
    return result


def latest_versions(session):
    result = [('Ссылка на документацию', 'Версия', 'Статус')]
    soup = get_soup(session, UrlConstants.MAIN_DOC_URL)
    tags_ul = soup.find(class_='sphinxsidebarwrapper').find_all('ul')
    for ul in tags_ul:
        if 'All versions' in ul.text:
            tags_a = ul.find_all('a')
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a in tqdm(tags_a,
                  total=len(tags_a),
                  desc=LiteralConstants.PARSER_PROCESS):
        text_match = re.search(pattern, a.text)
        if text_match:
            version, status = text_match.groups()
        else:
            version, status = a.text, ''
        result.append((a['href'], version, status))
    return result


def download(session):
    downloads_url = urljoin(UrlConstants.MAIN_DOC_URL, 'download.html')
    pdf_a4_link = get_soup(session, downloads_url).select_one(
        'div.body > table.docutils a[href$="pdf-a4.zip"]'
    )['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DirConstants.DOWNLOADS_DIR
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = get_response(session, archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)


def pep(session):
    logger_stack = []
    soup = get_soup(session, UrlConstants.PEP_MAIN_URL)
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

    status_codes = defaultdict(int)
    mismatches = []
    for num, url in tqdm(enumerate(relative_pep_urls),
                         total=len(relative_pep_urls),
                         desc=LiteralConstants.PARSER_PROCESS):
        try:
            soup = get_soup(session, urljoin(UrlConstants.PEP_MAIN_URL, url))
            page_status = soup.find('abbr').text
            if (page_status not in
               LiteralConstants.EXPECTED_STATUS.get(table_statuses[num])):
                mismatches.append(
                    'Несовпадение статуса: '
                    f'{urljoin(UrlConstants.PEP_MAIN_URL, url)} '
                    f'Статус на странице: {page_status} '
                    'Статус в списке: '
                    f'''{LiteralConstants.EXPECTED_STATUS
                         .get(table_statuses[num])}'''
                )
            status_codes[page_status] += 1
        except requests.RequestException as error:
            logger_stack.append(error)
    [logging.error(exception) for exception in logger_stack]
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
    try:
        configure_logging()
        logging.info(LiteralConstants.PARSER_STARTED)
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        session = CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        result = MODE_TO_FUNCTION[parser_mode](session)
        if result:
            control_output(result, args)
        logging.info(LiteralConstants.PARSER_FINISHED)
    except Exception as error:
        logging.exception(f'{LiteralConstants.PARSER_EXCEPTION} {error}',
                          stack_info=True)


if __name__ == '__main__':
    main()
