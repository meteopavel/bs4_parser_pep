import pytest

from pathlib import Path

BASE_DIR = Path(__name__).absolute().parent
MAIN_DIR = BASE_DIR / 'src'


@pytest.fixture
def results_dir():
    return [
        d for d in MAIN_DIR.iterdir() if d.is_dir() and d.name == 'results'
    ]


def test_results_dir_exists(results_dir):
    assert len(results_dir), (
        'Не обнаружена папка /results'
    )


def test_csv_files(results_dir):
    csv_files = [
        file for file in results_dir[0].iterdir() if file.glob('*.csv')
    ]

    assert len(csv_files), (
        'В папке results не обнаружен csv файл. '
        'Сохраните результаты работы парсера '
        'в csv-файле в папке results.'
    )
    assert not len(csv_files) > 1, (
        'Папка results содержит более одного файла. '
        'Оставьте в этой директории только один файл с результатами парсинга.'
    )
