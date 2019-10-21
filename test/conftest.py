import pytest
from pakselenium import Browser
from paksportgrab.grabber import Grabber

from . import credentials


@pytest.fixture(scope='session')
def browser() -> Browser:
    b = Browser()
    b.initChrome('C:/python/driver/chromedriver.exe', headless=True)
    return b


@pytest.fixture(scope='session')
def grabber(browser) -> Grabber:
    g = Grabber(browser, cookiePath='C:/python/cookies/')
    g.login(credentials.username, credentials.password)
    return g
