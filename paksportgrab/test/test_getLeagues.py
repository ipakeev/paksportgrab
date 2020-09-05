import copy
import datetime

import pytest

from paksportgrab.grabber import Grabber


@pytest.fixture(scope='module')
def sport():
    return 'baseball'


@pytest.fixture(scope='module')
def date():
    return datetime.date(2020, 9, 3)


@pytest.fixture(scope='class')
def leagues(grabber: Grabber, sport, date):
    return grabber.get_leagues(sport, date)


@pytest.mark.usefixtures('leagues')
class TestSportGrid:

    def test_reachedPage(self, grabber: Grabber, sport, date):
        sportGrid = grabber.sport_grid
        assert sportGrid.get_current_sport() == sport
        assert sportGrid.get_current_date() == date
        assert sportGrid.is_loaded_grid()
        assert sportGrid.is_switched_to_events()
        assert not sportGrid.is_switched_to_kick_off_time()
        assert not sportGrid.is_empty()
        assert not sportGrid.is_reload()

    def test_switch(self, grabber: Grabber):
        sportGrid = grabber.sport_grid
        sportGrid.switch_to_kick_off_time()
        assert not sportGrid.is_switched_to_events()
        assert sportGrid.is_switched_to_kick_off_time()
        sportGrid.switch_to_events()
        assert sportGrid.is_switched_to_events()
        assert not sportGrid.is_switched_to_kick_off_time()

    def test_sport(self, leagues):
        assert len(leagues) == 5

    def test_league(self, leagues, sport):
        league = leagues[2]
        assert league.sport == sport
        assert league.country == 'South Korea'
        assert league.league == 'KBO'
        assert league.league_url == 'https://www.oddsportal.com/baseball/south-korea/kbo/results/'
        assert len(league.next_matches) == 5

    def test_match(self, leagues, date):
        league = leagues[2]
        match = league.next_matches[0]
        assert match.sport == league.sport
        assert match.country == league.country
        assert match.league == league.league

        assert match.date == date
        assert match.time == datetime.time(12, 30)
        assert match.teams == ['LG Twins', 'NC Dinos']
        assert match.url == 'https://www.oddsportal.com/baseball/south-korea/kbo/lg-twins-nc-dinos-z5aH7qtI/'
        assert match.id == 'z5aH7qtI'
        assert match.score_string == '6:5'
        assert match.odds == {}
        assert 11 <= match.bk_num <= 16
        assert match.finished

    def test_matchSets(self, leagues):
        league = leagues[2]
        match = copy.deepcopy(league.next_matches[0])

        match.set_not_started()
        assert match.not_started
        assert not match.live
        assert not match.finished
        assert not match.canceled

        match.set_live()
        assert not match.not_started
        assert match.live
        assert not match.finished
        assert not match.canceled

        match.set_finished()
        assert not match.not_started
        assert not match.live
        assert match.finished
        assert not match.canceled

        match.set_canceled()
        assert not match.not_started
        assert not match.live
        assert not match.finished
        assert match.canceled
