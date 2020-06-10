import pytest
import datetime
import copy
from paksportgrab.grabber import Grabber


@pytest.fixture(scope='module')
def sport():
    return 'baseball'


@pytest.fixture(scope='module')
def date():
    return datetime.date(2020, 6, 10)


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
        assert len(leagues) == 4

    def test_league(self, leagues, sport):
        league = leagues[1]
        assert league.sport == sport
        assert league.country == 'South Korea'
        assert league.league == 'KBO'
        assert league.leagueUrl == 'https://www.oddsportal.com/baseball/south-korea/kbo/results/'
        assert len(league.nextMatches) == 4

    def test_match(self, leagues, date):
        league = leagues[1]
        match = league.nextMatches[0]
        assert match.sport == league.sport
        assert match.country == league.country
        assert match.league == league.league

        assert match.date == date
        assert match.time == datetime.time(12, 30)
        assert match.teams == ['Lotte Giants', 'Hanwha Eagles']
        assert match.url == 'https://www.oddsportal.com/baseball/south-korea/kbo/lotte-giants-hanwha-eagles-CxsNnaBL/'
        assert match.id == 'CxsNnaBL'
        assert match.scoreString == '12:2'
        assert match.odds == {}
        assert match.bkNum == 11
        assert match.finished

    def test_matchSets(self, leagues):
        league = leagues[1]
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
