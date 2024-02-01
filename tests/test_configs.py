import pytest
import argparse
try:
    from src import configs
except ModuleNotFoundError:
    assert False, 'Убедитесь что в директории `src` есть файл `configs.py`'
except ImportError:
    assert False, 'Убедитесь что в директории `src` есть файл `configs.py`'


def test_configs_file():
    assert hasattr(configs, 'configure_argument_parser'), (
        'Добавьте функцию `configure_argument_parser` в `configs.py` модуль.'
    )
    assert hasattr(configs, 'configure_logging'), (
        'Добавьте функцию `configure_logging` в `configs.py` модуль.'
    )


@pytest.mark.parametrize('action, option_string, dest, choises, help_str', [
    (
        argparse._StoreAction, [], 'mode',
        ['whats-new', 'latest-versions', 'download', 'pep'],
        'Режимы работы парсера'
    ),
    (
        argparse._StoreTrueAction, ['-c', '--clear-cache'], 'clear_cache',
        None, 'Очистка кеша'
    ),
    (
        argparse._StoreAction, ['-o', '--output'], 'output',
        ('pretty', 'file'),
        'Дополнительные способы вывода данных'
    ),
])
def test_configure_argument_parser(
        action,
        option_string,
        dest,
        choises,
        help_str
):
    got = configs.configure_argument_parser(choises)
    got_actions = [
        g for g in got._actions
        if isinstance(g, action) and g.dest == dest
    ]
    if not len(got_actions):
        assert False, (
            f'Проверьте аргументы парсера. Cli аргумент {dest} не '
            'соответсвует заданию'
        )
    got_action = got_actions[0]
    assert isinstance(got_action, action)
    assert got_action.option_strings == option_string, (
        f'Укажите для аргумента {got_action.help} имя или флаг={option_string}'
    )
    assert got_action.dest == dest, (
        f'Укажите имя атрибута для {got_action.help}'
    )
    assert got_action.choices == choises, (
        f'Укажите выбор для cli аргумента {got_action.dest}'
    )
    assert got_action.help == help_str, (
        f'Укажите help-строку cli аргумента {got_action.dest}'
    )
