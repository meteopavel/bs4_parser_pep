from pathlib import Path

BASE_DIR = Path(__file__).parent

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_MAIN_URL = 'https://peps.python.org/'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}


class DirConstants:
    LOG_DIR = BASE_DIR / 'logs'
    DOWNLOADS_DIR = 'downloads'
    RESULTS_DIR = 'results'
    LOG_FILE = LOG_DIR / 'parser.log'


class LiteralConstants:
    EXPECTED_STATUS = EXPECTED_STATUS
    PARSER_STARTED = 'Запуск парсера'
    PARSER_PROCESS = 'Парсинг в процессе'
    PARSER_FINISHED = 'Парсинг завершён'
    PARSER_EXCEPTION = 'При парсинге возникла ошибка'
    PRETTY_OUTPUT_MODE = 'pretty'
    FILE_OUTPUT_MODE = 'file'
    FILE_DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
    LOGGER_DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
    LOGGER_FORMAT = (
        '%(levelname)s - %(asctime)s - %(lineno)s - %(funcName)s - '
        '%(message)s - %(name)s')


class UrlConstants:
    MAIN_DOC_URL = MAIN_DOC_URL
    PEP_MAIN_URL = PEP_MAIN_URL
