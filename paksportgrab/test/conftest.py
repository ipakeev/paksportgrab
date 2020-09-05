import pytest
from pakselenium import Browser

from paksportgrab.grabber import Grabber
from . import credentials


@pytest.fixture(scope='session')
def browser() -> Browser:
    b = Browser()
    b.init_chrome('D:/sport/work/chromedriver.exe')
    return b


@pytest.fixture(scope='session')
def grabber(browser) -> Grabber:
    g = Grabber(browser, cookie_path='D:/sport/work/')
    g.login(credentials.username, credentials.password)
    return g
