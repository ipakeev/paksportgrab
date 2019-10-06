import pytest
import copy
from paksportgrab.grabber import Grabber


@pytest.fixture(scope='module')
def sport():
    return 'baseball'


@pytest.fixture(scope='module')
def date():
    return '20190923'


@pytest.fixture(scope='class')
def leagues(grabber: Grabber, sport, date):
    return grabber.getLeagues(sport, date)


@pytest.mark.usefixtures('leagues')
class TestSportGrid:

    def test_reachedPage(self, grabber: Grabber, sport, date):
        sportGrid = grabber.sportGrid
        assert sportGrid.getCurrentSport() == sport
        assert sportGrid.getCurrentDate() == date
        assert sportGrid.isLoadedGrid()
        assert sportGrid.isSwitchedToEvents()
        assert not sportGrid.isSwitchedToKickOffTime()
        assert not sportGrid.isEmpty()
        assert not sportGrid.isReload()

    def test_switch(self, grabber: Grabber):
        sportGrid = grabber.sportGrid
        sportGrid.switchToKickOffTime()
        assert not sportGrid.isSwitchedToEvents()
        assert sportGrid.isSwitchedToKickOffTime()
        sportGrid.switchToEvents()
        assert sportGrid.isSwitchedToEvents()
        assert not sportGrid.isSwitchedToKickOffTime()

    def test_sport(self, leagues):
        assert len(leagues) == 5

    def test_league(self, leagues, sport):
        league = leagues[0]
        assert league.sport == sport
        assert league.country == 'Cuba'
        assert league.league == 'Serie Nacional'
        assert league.leagueUrl == 'https://www.oddsportal.com/baseball/cuba/serie-nacional/results/'
        assert len(league.nextMatches) == 7

    def test_match(self, leagues, date):
        league = leagues[0]
        match = league.nextMatches[0]
        assert match.sport == league.sport
        assert match.country == league.country
        assert match.league == league.league

        assert match.date == date
        assert match.time == '21:00'
        assert match.teams == ['Villa Clara', 'Sancti Spiritus']
        assert match.url == 'https://www.oddsportal.com/baseball/cuba/serie-nacional/villa-clara-sancti-spiritus-88bjyIXl/'
        assert match.id == '88bjyIXl'
        assert match.score == '5:0'
        assert match.odds == {'1X2': {'1': 2.17, '2': 1.64}}
        assert match.bkNum == 2
        assert match.finished

    def test_matchSets(self, leagues):
        league = leagues[0]
        match = copy.deepcopy(league.nextMatches[0])

        match.setNotStarted()
        assert match.notStarted
        assert not match.live
        assert not match.finished
        assert not match.canceled

        match.setLive()
        assert not match.notStarted
        assert match.live
        assert not match.finished
        assert not match.canceled

        match.setFinished()
        assert not match.notStarted
        assert not match.live
        assert match.finished
        assert not match.canceled

        match.setCanceled()
        assert not match.notStarted
        assert not match.live
        assert not match.finished
        assert match.canceled
