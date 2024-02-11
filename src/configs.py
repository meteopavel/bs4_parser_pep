import argparse
import logging
from logging.handlers import RotatingFileHandler

from constants import LiteralConstants, DirConstants


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
            LiteralConstants.PRETTY_OUTPUT_MODE,
            LiteralConstants.FILE_OUTPUT_MODE
        ),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging():
    log_dir = DirConstants.LOG_DIR
    log_dir.mkdir(exist_ok=True)
    log_file = DirConstants.LOG_FILE
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=5,
        encoding='utf-8'
    )
    logging.basicConfig(
        datefmt=LiteralConstants.LOGGER_DATETIME_FORMAT,
        format=LiteralConstants.LOGGER_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
