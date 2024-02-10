import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import BASE_DIR


def configure_argument_parser(modes):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode',
        choices=modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=(
            'pretty',
            'file'
        ),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging():
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'parser.log'
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=5,
        encoding='utf-8'
    )
    logging.basicConfig(
        datefmt='%d.%m.%Y %H:%M:%S',
        format=(
            '%(levelname)s - %(asctime)s - %(lineno)s - %(funcName)s - '
            '%(message)s - %(name)s'
        ),
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
