import pytest
import requests
import requests_mock
import bs4
from conftest import MAIN_DOC_URL
try:
    from src import utils
except ModuleNotFoundError:
    assert False, 'Убедитесь что в директории `src` есть файл `utils.py`'
except ImportError:
    assert False, 'Убедитесь что в директории `src` есть файл `utils.py`'


def test_find_tag(soup):
    got = utils.find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    assert isinstance(got, bs4.element.Tag), (
        'Функция `find_tag` в модуле `utils.py` должна возвращать искомый тег'
    )
    assert (
        '<section id="what-s-new-in-python">' in got.__str__()
    ), (
        'Функция `find_tag` модуля `utils.py` '
        'не вернула ожидаемый <section> с `id=what-s-new-in-python`'
    )


def test_find_tag_exception(soup):
    with pytest.raises(BaseException) as excinfo:
        utils.find_tag(soup, 'unexpected')
    assert excinfo.typename == 'ParserFindTagException', (
        'Функция `find_tag` в модуле `utils.py` в случае '
        'отсутствия искомого тэга'
        'должна выбросить нестандартное исключение `ParserFindTagException`'
    )
    msg = 'Не найден тег unexpected None'
    assert msg in str(excinfo.value), (
        f'Нестандартное исключение должно показывать сообщение: `{msg}`'
    )


def test_get_response(mock_session):
    with requests_mock.Mocker() as mock:
        mock.get(
            MAIN_DOC_URL + 'unexisting_page/',
            text='You are breathtaken',
            status_code=200
        )
        got = utils.get_response(
            mock_session,
            MAIN_DOC_URL + 'unexisting_page/'
        )
        assert isinstance(got, requests.models.Response), (
            'Убедитесь что функция `get_response` в модуле `utils.py` '
            'делает запрос к странице и возвращает ответ. \n'
            'Кстати: You are breathtaken!'
        )
