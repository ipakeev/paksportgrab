import pytest

from paksportgrab.oddsportal.config import names
from paksportgrab.oddsportal.config.selector import reCompiled
from paksportgrab.oddsportal import utils


def test_names():
    for key, value in names.sportName.items():
        if ' ' in key:
            assert key.replace(' ', '-').lower() == value


def test_re_date():
    def control(s):
        v = reCompiled.date.findall(s)
        assert len(v) == 1
        assert v[0] == target

    target = ('19', 'Sep', '2019')
    control('19 Sep 2019')
    control('fd 19 Sep 2019 fd')
    control('23 19 Sep 2019 09')


def test_re_dateTime():
    def control(s):
        v = reCompiled.dateTime.findall(s)
        assert len(v) == 1
        assert v[0] == target

    target = ('19', 'Sep', '2019', '20:00')
    control('19 Sep 2019 20:00')
    control('fd 19 Sep 2019 . 20:00 fd')
    control('23 19 Sep 2019  20:00 09')


def test_re_oddValue():
    def control(s, target):
        v = reCompiled.oddValue.findall(s)
        assert len(v) == 1
        assert v[0] == target

    control('Over/Under +1.5', '+1.5')
    control('Over/Under +1.55', '+1.55')
    control('Over/Under -1.5', '-1.5')
    control('Over/Under +1', '+1')
    control('Over/Under -1', '-1')
    control('Over/Under 0', '0')


def test_sportName():
    assert utils.getSportName('Soccer') == names.sportName['Soccer']
    with pytest.raises(KeyError):
        utils.getSportName('soccer')


def test_matchTabName():
    assert utils.getMatchTabName('Over/Under') == names.total
    assert utils.getMatchTabName('') is None
    with pytest.raises(KeyError):
        utils.getMatchTabName('ou')


def test_matchSubTabName():
    assert utils.getMatchSubTabName('Full Time') == names.ft
    assert utils.getMatchSubTabName('') is None
    with pytest.raises(KeyError):
        utils.getMatchSubTabName('ft')


def test_matchId():
    url = 'https://www.oddsportal.com/soccer/spain/laliga/atl-madrid-real-madrid-I9OmRkES/'
    assert utils.getMatchId(url) == 'I9OmRkES'


def test_dateFromString():
    assert utils.getDateFromString('19 Sep 2019') == '20190919'


def test_dateSportUrl():
    assert utils.getDateSportUrl('soccer', '20190919') == f'{names.baseUrl}matches/soccer/20190919/'
