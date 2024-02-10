import argparse


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
    pass
