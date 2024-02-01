import pytest
from pathlib import Path
try:
    from src import main
except ModuleNotFoundError:
    assert False, 'Убедитесь что в директории `src` есть файл `main.py`'
except ImportError:
    assert False, 'Убедитесь что в директории `src` есть файл `main.py`'


def test_main_file():
    assert hasattr(main, 'whats_new'), (
        'Добавьте функцию `whats_new` в модуль `main.py`.'
    )
    assert hasattr(main, 'latest_versions'), (
        'Добавьте функцию `latest_versions` в модуль `main.py`.'
    )
    assert hasattr(main, 'download'), (
        'Добавьте функцию `download` в модуль `main.py`.'
    )
    assert hasattr(main, 'pep'), (
        'Добавьте функцию `pep` в модуль `main.py`.'
    )
    assert hasattr(main, 'MODE_TO_FUNCTION'), (
        'Добавьте словарь `MODE_TO_FUNCTION` с перечнем режимов '
        'работы парсера.'
    )
    assert hasattr(main, 'main'), (
        'Добавьте функцию `main` в модуль `main.py`.'
    )


def test_whats_new(mock_session):
    got = main.whats_new(mock_session)
    header = ('Ссылка на статью', 'Заголовок', 'Редактор, Автор')
    assert isinstance(got, list), (
        'Функция `whats_new` должна возвращать объект типа `list`'
    )
    assert len(got) > 0, (
        'Убедитесь что функция `whats_new` модуля `main.py` '
        'возвращает непустой список'
    )
    assert isinstance(got[0], tuple), (
        'Функция `whats_new` дожна вернуть список `result`, '
        'элементами которого должны быть объекты типа `tuple`'
    )
    assert header in got, (
        'В функции `whats_new` в списке `result` первым элементом '
        'должен быть кортеж '
        '(`Ссылка на статью`, `Заголовок`, `Редактор, Автор`)'
    )


@pytest.mark.skip()
def test_latest_versions(mock_session):
    got = main.latest_versions(mock_session)
    assert isinstance(got, list), (
        'Функция `latest_versions` должна возвращать объект типа `list`'
    )
    assert isinstance(got[0], tuple), (
        'Функция `latest_versions` должна вернуть список `result`, '
        'элементами которого должны быть объекты типа `tuple`'
    )
    header = ('Ссылка на документацию', 'Версия', 'Статус')
    answer = [
        ('Ссылка на документацию', 'Версия', 'Статус'),
        ('https://docs.python.org/3.12/', '3.12', 'in development'),
        ('https://docs.python.org/3.11/', '3.11', 'pre-release'),
        ('https://docs.python.org/3.10/', '3.10', 'stable'),
        ('https://docs.python.org/3.9/', '3.9', 'stable'),
        ('https://docs.python.org/3.8/', '3.8', 'security-fixes'),
        ('https://docs.python.org/3.7/', '3.7', 'security-fixes'),
        ('https://docs.python.org/3.6/', '3.6', 'EOL'),
        ('https://docs.python.org/3.5/', '3.5', 'EOL'),
        ('https://docs.python.org/2.7/', '2.7', 'EOL'),
        ('https://www.python.org/doc/versions/', 'All versions', '')
    ]
    assert header in got, (
        'В функции `latest_versions` в списке results '
        'первым элементов должен быть кортеж '
        '`Ссылка на документацию, Версия, Статус`'
    )
    assert got == answer, (
        'Функция `latest_versions` должна возвращать '
        f'объект вида ```{answer}```'
    )


def test_download(monkeypatch, tmp_path, mock_session):
    mock_base_dir = Path(tmp_path)
    monkeypatch.setattr(main, 'BASE_DIR', mock_base_dir)
    got = main.download(mock_session)
    dirs = [
        directory for directory in mock_base_dir.iterdir()
        if directory.is_dir() and directory.name == 'downloads'
    ]

    assert len(dirs) != 0, (
        'Убедитесь что для хранения архивов с документацией Python в '
        'директории `src` создаётся директория `downloads` '
    )
    output_files = [
        f for f in mock_base_dir.glob('**/*') if str(f).endswith('.zip')
    ]
    assert len(output_files) != 0, (
        'Убедитесь что архив с документацией Python загружается'
        'в директорию `src/downloads`  '
    )
    assert got is None, (
        'Функция `download` в модуле `main.py` не должна возвращать значение.',
        'Функция должна только загружать и сохранять архив.'
    )


def test_mode_to_function():
    got = main.MODE_TO_FUNCTION
    assert isinstance(got, dict), (
        'В модуле `main.py` объект `MODE_TO_FUNCTION` должен быть словарем'
    )
    for name_func, func in got.items():
        assert isinstance(name_func, str), (
            'Убедитесь, чтобы в модуле `main.py` в словаре `MODE_TO_FUNCTION` '
            f'{name_func} - это строка.'
        )
        assert (
            name_func in ['whats-new', 'latest-versions', 'download', 'pep']
        ), (
            'В модуле `main.py` в объекте `MODE_TO_FUNCTION` '
            f'нет ключа `{name_func}`'
        )
        assert callable(func), (
            'Убедитесь, что в модуле `main.py` в объекте `MODE_TO_FUNCTION` '
            f'`{func}` - это функция.'
        )
        assert (
            func.__name__ in [
                'whats_new', 'latest_versions', 'download', 'pep'
            ]
        ), (
            'В модуле `main.py` в объекте `MODE_TO_FUNCTION` '
            f'нет значения {func}'
        )
