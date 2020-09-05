import datetime
from typing import List

import pytest

from paksportgrab.grabber import Grabber
from paksportgrab.oddsportal.units.match import Match


# --------------------------------------------------------------


@pytest.fixture()
def getPage1(grabber: Grabber):
    ms = grabber.get_matches('https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/results/',
                             till_match_id='QVBrfakT')
    return ms


@pytest.fixture(scope='class')
def matches_tillPage1(grabber: Grabber):
    ms = grabber.get_matches('https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/results/',
                             till_match_id='QVBrfakT')
    return ms


@pytest.fixture(scope='class')
def matches_tillPage3(grabber: Grabber):
    ms = grabber.get_matches('https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/results/',
                             till_match_id='67rV8htF')
    return ms


@pytest.fixture(scope='class')
def matches_tillLast(grabber: Grabber):
    ms = grabber.get_matches('https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/results/')
    return ms


# --------------------------------------------------------------


@pytest.mark.usefixtures('getPage1')
def test_nextPage(grabber: Grabber):
    assert '1' not in grabber.league_grid.get_navigation_buttons()
    grabber.league_grid.next_page()
    assert '1' in grabber.league_grid.get_navigation_buttons()


@pytest.mark.usefixtures('getPage1')
def test_lastPage(grabber: Grabber):
    for _ in range(7):
        grabber.league_grid.next_page()
    assert '8' not in grabber.league_grid.get_navigation_buttons()
    assert grabber.league_grid.is_end_of_season()


# --------------------------------------------------------------


@pytest.mark.usefixtures('matches_tillPage1')
class TestTillPage1:

    def test_common(self, grabber: Grabber):
        assert grabber.league_grid.is_visible_season_tabs()
        assert grabber.league_grid.is_loaded_grid()
        assert not grabber.league_grid.is_end_of_season()
        assert not grabber.league_grid.is_empty()
        assert not grabber.league_grid.is_reload()
        assert grabber.league_grid.is_visible_navigation_buttons()

    def test_matchesLength(self, matches_tillPage1):
        assert len(matches_tillPage1) == 50

    def test_SCL(self, grabber: Grabber):
        assert grabber.league_grid.get_SCL() == ('Soccer', 'Argentina', 'Superliga')

    def test_currentSeasonName(self, grabber: Grabber):
        assert grabber.league_grid.get_current_season_name() == '2017/2018'

    def test_seasons(self, grabber: Grabber):
        seasons = grabber.league_grid.get_season_tabs()
        assert seasons[0].text == '2017/2018'

    def test_navigation(self, grabber: Grabber):
        btns = grabber.league_grid.get_navigation_buttons()
        assert '1' not in btns
        assert '2' in btns


@pytest.mark.usefixtures('matches_tillPage3')
class TestTillPage3:

    def test_common(self, grabber: Grabber):
        assert not grabber.league_grid.is_end_of_season()

    def test_matchesLength(self, matches_tillPage3):
        assert len(matches_tillPage3) == 150

    def test_navigation(self, grabber: Grabber):
        btns = grabber.league_grid.get_navigation_buttons()
        assert '1' in btns
        assert '3' not in btns

    def test_firstMatch(self, matches_tillPage3: List[Match]):
        match = matches_tillPage3[0]
        with pytest.raises(AttributeError):
            _ = match.sport
        with pytest.raises(AttributeError):
            _ = match.country
        with pytest.raises(AttributeError):
            _ = match.league

        assert match.season == '2017/2018'
        assert match.date == datetime.date(2018, 5, 15)
        assert match.time == datetime.time(3, 15)
        assert match.teams == ['Gimnasia L.P.', 'Newells Old Boys']
        assert match.url == 'https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/gimnasia-l-p-newells-old-boys-QVBrfakT/'
        assert match.id == 'QVBrfakT'
        assert match.score_string == '2:0'
        assert match.odds == {}
        assert 10 <= match.bk_num <= 14
        assert match.finished

    def test_lastMatch(self, matches_tillPage3: List[Match]):
        match = matches_tillPage3[-1]

        assert match.season == '2017/2018'
        assert match.date == datetime.date(2018, 2, 25)
        assert match.time == datetime.time(1, 15)
        assert match.teams == ['Velez Sarsfield', 'River Plate']
        assert match.url == 'https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/velez-sarsfield-river-plate-xGt8WUHH/'
        assert match.id == 'xGt8WUHH'
        assert match.score_string == '1:0'
        assert match.odds == {}
        assert 10 <= match.bk_num <= 14
        assert match.finished


@pytest.mark.skip()
@pytest.mark.usefixtures('matches_tillLast')
class TestTillLast:

    def test_common(self, grabber: Grabber):
        assert grabber.league_grid.is_end_of_season()
        assert grabber.league_grid.is_empty()

    def test_lastMatch(self, matches_tillLast: List[Match]):
        match = matches_tillLast[-1]
        with pytest.raises(AttributeError):
            _ = match.sport
        with pytest.raises(AttributeError):
            _ = match.country
        with pytest.raises(AttributeError):
            _ = match.league

        assert match.season == '2016/2017'
        assert match.date == '20160920'
        assert match.time == '01:00'
        assert match.teams == ['Tigre', 'Huracan']
        assert match.url == 'https://www.oddsportal.com/soccer/argentina/primera-division-2016-2017/tigre-huracan-Mg9lwkhO/'
        assert match.id == 'Mg9lwkhO'
        assert match.score_string == '1:1'
        assert match.odds == {'1X2': {'1': 2.9, 'X': 2.2, '2': 3.66}}
        assert match.bk_num == 1
        assert match.finished
