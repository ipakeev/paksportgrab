import pytest
from paksportgrab.grabber import Grabber

from . import credentials


def test_userKwargs(grabber: Grabber):
    assert grabber.user.username == credentials.username
    assert grabber.user.password == credentials.password


@pytest.mark.skip()
def test_userLogin(grabber: Grabber):
    assert grabber.user.isLoggedIn()
    grabber.user.logout()
    assert not grabber.user.isLoggedIn()
    grabber.user.login()
    assert grabber.user.isLoggedIn()
