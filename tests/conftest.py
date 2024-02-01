import pytest
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import requests_mock
from argparse import Namespace
from typing import List, Tuple

from requests_cache import CachedSession, ALL_METHODS
from requests_mock import Adapter

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
SRC_DIR = BASE_DIR / 'src'
sys.path.append(str(BASE_DIR))
sys.path.append(str(SRC_DIR))

MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://www.python.org/dev/peps/'


precode_files = ['constants.py', 'main.py', 'utils.py']
src_dir_files = [file.name for file in SRC_DIR.rglob('*.py')]
try:
    from src import utils, configs, main
except (ImportError, ModuleNotFoundError, NameError):
    for file in precode_files:
        assert file in src_dir_files, f'Отсутсвует файл {file}'


def pytest_make_parametrize_id(config, val):
    return repr(val)


@pytest.fixture(scope='function')
def tempfile_session() -> CachedSession:
    """Get a CachedSession using a temporary SQLite db"""
    yield CachedSession(
        backend='memory',
        allowable_methods=ALL_METHODS,
    )


def get_mock_adapter() -> Adapter:
    adapter = Adapter()
    adapter.register_uri(
        requests_mock.ANY,
        requests_mock.ANY,
        headers={'Content-Type': 'text/plain'},
        text='You are breathtaken',
        status_code=200,
    )
    adapter.register_uri(
        'GET',
        PEP_URL,
        text='No, you are breathtaken!',
        status_code=200,
    )
    return adapter


def mount_mock_adapter(session: CachedSession) -> CachedSession:
    adapter = get_mock_adapter()
    MOCK_PROTOCOLS = ['mock://', 'http+mock://', 'https+mock://']
    for protocol in MOCK_PROTOCOLS:
        session.mount(protocol, adapter)
    session.mock_adapter = adapter
    return session


@pytest.fixture(scope='function')
def mock_session(tempfile_session) -> CachedSession:
    yield mount_mock_adapter(tempfile_session)


@pytest.fixture
def response_page(mock_session):
    def _response_page(page):
        response = mock_session.get(page)
        response.encoding = 'utf-8'
        return response.text
    return _response_page


@pytest.fixture
def soup(response_page):
    response = response_page(MAIN_DOC_URL + '/whatsnew')
    return BeautifulSoup(response, features='lxml')


@pytest.fixture
def pep_namespace():
    return Namespace(mode='pep', clear_cache=False, output='file')


def converting(what_convert: List[Tuple[List[int]]]) -> List[Tuple]:
    converted = []
    for lis in what_convert:
        new_s = []
        for tup in lis:
            new = ''.join(map(chr, tup))
            new_s.append(new)
        converted.append(tuple(new_s))
    return converted


@pytest.fixture
def records():
    def _records(mode: str):
        from tests.fixture_data.results import results
        result = results[mode]
        return converting(result)
    return _records
