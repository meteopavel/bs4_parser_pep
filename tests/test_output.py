from datetime import datetime
from typing import Optional
from pathlib import Path
import pytest
from argparse import Namespace
try:
    from src import outputs
except ModuleNotFoundError:
    assert False, 'Убедитесь что в директории `src` есть файл `outputs.py`'
except ImportError:
    assert False, 'Убедитесь что в директории `src` есть файл `outputs.py`'


def cli_args(mode: str, output_format: Optional[str]) -> Namespace:
    return Namespace(mode=mode, output=output_format)


@pytest.mark.parametrize('cli_arg', [
    cli_args('whats-new', None),
    cli_args('latest-versions', None),
    cli_args('pep', None),
])
def test_control_output_default(capsys, records, cli_arg):
    records = records(cli_arg.mode)
    outputs.control_output(records, cli_arg)
    captured_out, _ = capsys.readouterr()
    if cli_arg.mode == 'pep':
        records = '\n'.join([f'{k} {v}' for k, v in records])
    else:
        records = '\n'.join([f'{k} {v} {c}' for k, v, c in records])
    assert records in captured_out, f'Проверьте вывод в консоль для {cli_arg}'


@pytest.mark.parametrize('cli_arg, part_output', [
    (cli_args('whats-new', 'pretty'), 'New'),
    (cli_args('latest-versions', 'pretty'), 'docs'),
    (cli_args('pep', 'pretty'), 'Active'),
])
def test_control_output_pretty(capsys, records, cli_arg, part_output):
    records = records(cli_arg.mode)
    outputs.control_output(records, cli_arg)
    captured_out, _ = capsys.readouterr()
    assert '------' in captured_out, f'Проверьте вывод в консоль для {cli_arg}'
    assert part_output in captured_out, (
        f'Некорректный вывод для cli аргумента {cli_arg}.'
    )


@pytest.mark.parametrize('cli_arg', [
    cli_args('whats-new', 'file'),
    cli_args('latest-versions', 'file'),
    cli_args('pep', 'file'),
])
def test_control_output_file(monkeypatch, tmp_path, records, cli_arg):
    mock_base_dir = Path(tmp_path)
    monkeypatch.setattr(outputs, 'BASE_DIR', mock_base_dir)

    records = records(cli_arg.mode)
    outputs.control_output(records, cli_arg)
    dirs = [
        directory.name for directory in mock_base_dir.iterdir()
        if directory.is_dir()
    ]
    assert dirs == ['results'], (
        'Убедитесь что для сохранения файлов в директории '
        '`src` создается директория `results`'
    )
    output_files = [
        file for file in mock_base_dir.glob('**/*')
        if str(file).endswith('.csv')
    ]
    assert output_files[0].name == (
        f"{cli_arg.mode}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    ), (
        'Убедитесь что имя файла соотвествует паттерну '
        '<имя-режима_дата_в_формате_%Y-%m-%d_%H-%M-%S>.csv \n'
        'С форматами кодов вы можете познакомиться тут - \n'
        'https://docs.python.org/3/library/datetime.html?'
        'highlight=strftime#strftime-and-strptime-format-codes'
    )


def test_output_file():
    assert hasattr(outputs, 'control_output'), (
        'Напишите функцию `control_output` в модуле `output.py`'
    )
    assert hasattr(outputs, 'pretty_output'), (
        'Напишите функцию `pretty_output` в модуле `output.py`'
    )
    assert hasattr(outputs, 'file_output'), (
        'Напишите функцию `file_output` в модуле `output.py`'
    )
