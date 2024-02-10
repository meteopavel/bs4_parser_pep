# Проект парсинга pep
Парсер используется для парсинга веб-сайта документации Python и извлечения информации о последних версиях.

## Основные используемые инструменты
* Python
* BeautifulSoup
* requests_cache

## Развёртывание проекта на локальном компьютере
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:meteopavel/bs4_parser_pep.git
```
Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv venv
linux: source env/bin/activate
windows: source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Использование
```python
python src/main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}
```

## Автор
[Павел Найденов](https://github.com/meteopavel)