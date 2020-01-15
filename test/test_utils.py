import pytest
import datetime
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
    assert utils.getMatchTabName('Over/Under') == names.tab.total
    assert utils.getMatchTabName('') is None
    with pytest.raises(KeyError):
        utils.getMatchTabName('ou')


def test_matchSubTabName():
    assert utils.getMatchSubTabName('Full Time') == names.subTab.ft
    assert utils.getMatchSubTabName('') is None
    with pytest.raises(KeyError):
        utils.getMatchSubTabName('ft')


def test_matchId():
    url = 'https://www.oddsportal.com/soccer/spain/laliga/atl-madrid-real-madrid-I9OmRkES/'
    assert utils.getMatchId(url) == 'I9OmRkES'

    url = 'https://www.oddsportal.com/soccer/spain/laliga/atl-madrid-real-madrid-I9OmRkES/#over-under;3'
    assert utils.getMatchId(url) == 'I9OmRkES'


def test_dateSportUrl():
    date = datetime.date(2019, 9, 19)
    assert utils.getDateSportUrl('soccer', date) == f'{names.baseUrl}matches/soccer/20190919/'


def test_dateFromString():
    assert utils.getDateFromString('19 Sep 2019') == datetime.date(2019, 9, 19)
    assert utils.getDateFromString('Today, 19 Sep 2019, 18:00') == datetime.date(2019, 9, 19)


def test_dateTimeFromString():
    dt = datetime.datetime(2019, 9, 19, 18, 30)
    assert utils.getDateTimeFromString('Today, 19 Sep 2019, 18:30') == dt


def test_oddValue():
    assert utils.getOddValue('-1.75') == -1.75
    assert utils.getOddValue('-1.5') == -1.5
    assert utils.getOddValue('-1') == -1.0
    assert utils.getOddValue('-0') == 0.0
    assert utils.getOddValue('0') == 0.0
    assert utils.getOddValue('+0') == 0.0
    assert utils.getOddValue('1') == 1.0
    assert utils.getOddValue('+1') == 1.0
    assert utils.getOddValue('1.5') == 1.5
    assert utils.getOddValue('+1.5') == 1.5
    assert utils.getOddValue('1.75') == 1.75
    assert utils.getOddValue('+1.75') == 1.75


def test_isReachedUrl():
    target = 'https://www.oddsportal.com/matches/soccer/20200115/'
    assert utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/matches/soccer/20200115/')
    assert not utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/matches/hockey/20200115/')
    assert not utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/matches/soccer/20200125/')

    target = 'https://www.oddsportal.com/soccer/france/ligue-1/results/'
    assert utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/soccer/france/ligue-1/results/')
    assert not utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/hockey/france/ligue-1/results/')
    assert not utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/soccer/germany/ligue-1/results/')
    assert not utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/soccer/germany/ligue-1/results/#/page/2/')
    # assert not utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/soccer/france/ligue-2/results/')

    target = 'https://www.oddsportal.com/soccer/france/ligue-1/results/#/page/2/'
    assert utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/soccer/france/ligue-1/results/#/page/2/')
    assert not utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/soccer/france/ligue-1/results/')
    assert not utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/soccer/france/ligue-1/results/#/page/1/')
    assert not utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/soccer/germany/ligue-1/results/#/page/2/')
    # assert not utils.isReachedUrl(target).isEqual(
    # 'https://www.oddsportal.com/soccer/france/ligue-2/results/#/page/2/')

    target = 'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j3hAArYI/'
    assert utils.isReachedUrl(target).isEqual(
        'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j3hAArYI/')
    assert utils.isReachedUrl(target).isEqual(
        'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j3hAArYI/#over-under;3')
    assert not utils.isReachedUrl(target).isEqual(
        'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j2hAArYI/')

    target = 'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j3hAArYI/#over-under;3'
    assert utils.isReachedUrl(target).isEqual(
        'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j3hAArYI/#over-under;3')
    assert not utils.isReachedUrl(target).isEqual(
        'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j2hAArYI/#over-under;2')
