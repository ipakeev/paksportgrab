import datetime

import pytest

from paksportgrab.oddsportal import utils
from paksportgrab.oddsportal.config import names
from paksportgrab.oddsportal.config.selector import re_compiled


def test_names():
    for key, value in names.sport_name.items():
        if ' ' in key:
            assert key.replace(' ', '-').lower() == value


def test_re_date():
    def control(s):
        v = re_compiled.date.findall(s)
        assert len(v) == 1
        assert v[0] == target

    target = ('19', 'Sep', '2019')
    control('19 Sep 2019')
    control('fd 19 Sep 2019 fd')
    control('23 19 Sep 2019 09')


def test_re_date_time():
    def control(s):
        v = re_compiled.date_time.findall(s)
        assert len(v) == 1
        assert v[0] == target

    target = ('19', 'Sep', '2019', '20:00')
    control('19 Sep 2019 20:00')
    control('fd 19 Sep 2019 . 20:00 fd')
    control('23 19 Sep 2019  20:00 09')


def test_re_odd_value():
    def control(s, target):
        v = re_compiled.odd_value.findall(s)
        assert len(v) == 1
        assert v[0] == target

    control('Over/Under +1.5', '+1.5')
    control('Over/Under +1.55', '+1.55')
    control('Over/Under -1.5', '-1.5')
    control('Over/Under +1', '+1')
    control('Over/Under -1', '-1')
    control('Over/Under 0', '0')


def test_sport_name():
    assert utils.get_sport_name('Soccer') == names.sport_name['Soccer']
    with pytest.raises(KeyError):
        utils.get_sport_name('soccer')


def test_match_tab_name():
    assert utils.get_match_tab_name('Over/Under') == names.tab.total
    assert utils.get_match_tab_name('') is None
    with pytest.raises(KeyError):
        utils.get_match_tab_name('ou')


def test_match_sub_tab_name():
    assert utils.get_match_sub_tab_name('Full Time') == names.sub_tab.ft
    assert utils.get_match_sub_tab_name('') is None
    with pytest.raises(KeyError):
        utils.get_match_sub_tab_name('ft')


def test_match_id():
    url = 'https://www.oddsportal.com/soccer/spain/laliga/atl-madrid-real-madrid-I9OmRkES/'
    assert utils.get_match_id(url) == 'I9OmRkES'

    url = 'https://www.oddsportal.com/soccer/spain/laliga/atl-madrid-real-madrid-I9OmRkES/#over-under;3'
    assert utils.get_match_id(url) == 'I9OmRkES'


def test_date_sport_url():
    date = datetime.date(2019, 9, 19)
    assert utils.get_date_sport_url('soccer', date) == f'{names.base_url}matches/soccer/20190919/'


def test_date_from_string():
    assert utils.get_date_from_string('19 Sep 2019') == datetime.date(2019, 9, 19)
    assert utils.get_date_from_string('Today, 19 Sep 2019, 18:00') == datetime.date(2019, 9, 19)


def test_date_time_from_string():
    dt = datetime.datetime(2019, 9, 19, 18, 30)
    assert utils.get_date_time_from_string('Today, 19 Sep 2019, 18:30') == dt


def test_odd_value():
    assert utils.get_odd_value('-1.75') == -1.75
    assert utils.get_odd_value('-1.5') == -1.5
    assert utils.get_odd_value('-1') == -1.0
    assert utils.get_odd_value('-0') == 0.0
    assert utils.get_odd_value('0') == 0.0
    assert utils.get_odd_value('+0') == 0.0
    assert utils.get_odd_value('1') == 1.0
    assert utils.get_odd_value('+1') == 1.0
    assert utils.get_odd_value('1.5') == 1.5
    assert utils.get_odd_value('+1.5') == 1.5
    assert utils.get_odd_value('1.75') == 1.75
    assert utils.get_odd_value('+1.75') == 1.75


def test_is_reached_url():
    target = 'https://www.oddsportal.com/matches/soccer/20200115/'
    assert utils.is_reached_url(target).is_equal('https://www.oddsportal.com/matches/soccer/20200115/')
    assert not utils.is_reached_url(target).is_equal('https://www.oddsportal.com/matches/hockey/20200115/')
    assert not utils.is_reached_url(target).is_equal('https://www.oddsportal.com/matches/soccer/20200125/')

    target = 'https://www.oddsportal.com/soccer/france/ligue-1/results/'
    assert utils.is_reached_url(target).is_equal('https://www.oddsportal.com/soccer/france/ligue-1/results/')
    assert not utils.is_reached_url(target).is_equal('https://www.oddsportal.com/hockey/france/ligue-1/results/')
    assert not utils.is_reached_url(target).is_equal('https://www.oddsportal.com/soccer/germany/ligue-1/results/')
    assert not utils.is_reached_url(target).is_equal(
        'https://www.oddsportal.com/soccer/germany/ligue-1/results/#/page/2/')
    # assert not utils.isReachedUrl(target).isEqual('https://www.oddsportal.com/soccer/france/ligue-2/results/')

    target = 'https://www.oddsportal.com/soccer/france/ligue-1/results/#/page/2/'
    assert utils.is_reached_url(target).is_equal('https://www.oddsportal.com/soccer/france/ligue-1/results/#/page/2/')
    assert not utils.is_reached_url(target).is_equal('https://www.oddsportal.com/soccer/france/ligue-1/results/')
    assert not utils.is_reached_url(target).is_equal(
        'https://www.oddsportal.com/soccer/france/ligue-1/results/#/page/1/')
    assert not utils.is_reached_url(target).is_equal(
        'https://www.oddsportal.com/soccer/germany/ligue-1/results/#/page/2/')
    # assert not utils.isReachedUrl(target).isEqual(
    # 'https://www.oddsportal.com/soccer/france/ligue-2/results/#/page/2/')

    target = 'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j3hAArYI/'
    assert utils.is_reached_url(target).is_equal(
        'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j3hAArYI/')
    assert utils.is_reached_url(target).is_equal(
        'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j3hAArYI/#over-under;3')
    assert not utils.is_reached_url(target).is_equal(
        'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j2hAArYI/')

    target = 'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j3hAArYI/#over-under;3'
    assert utils.is_reached_url(target).is_equal(
        'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j3hAArYI/#over-under;3')
    assert not utils.is_reached_url(target).is_equal(
        'https://www.oddsportal.com/soccer/france/ligue-1/nantes-toulouse-j2hAArYI/#over-under;2')
