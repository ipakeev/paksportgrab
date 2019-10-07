import pytest
from typing import List
from paksportgrab.grabber import Grabber
from paksportgrab.oddsportal.units.match import Match


# --------------------------------------------------------------


@pytest.fixture()
def getPage1(grabber: Grabber):
    ms = grabber.getMatches('https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/results/',
                            tillMatchId='QVBrfakT')
    return ms


@pytest.fixture(scope='class')
def matches_tillPage1(grabber: Grabber):
    ms = grabber.getMatches('https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/results/',
                            tillMatchId='QVBrfakT')
    return ms


@pytest.fixture(scope='class')
def matches_tillPage3(grabber: Grabber):
    ms = grabber.getMatches('https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/results/',
                            tillMatchId='67rV8htF')
    return ms


@pytest.fixture(scope='class')
def matches_tillLast(grabber: Grabber):
    ms = grabber.getMatches('https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/results/')
    return ms


# --------------------------------------------------------------


@pytest.mark.usefixtures('getPage1')
def test_nextPage(grabber: Grabber):
    assert '1' not in grabber.leagueGrid.getNavigationButtons()
    grabber.leagueGrid.nextPage()
    assert '1' in grabber.leagueGrid.getNavigationButtons()


@pytest.mark.usefixtures('getPage1')
def test_lastPage(grabber: Grabber):
    for _ in range(7):
        grabber.leagueGrid.nextPage()
    assert '8' not in grabber.leagueGrid.getNavigationButtons()
    assert grabber.leagueGrid.isEndOfSeason()


# --------------------------------------------------------------


@pytest.mark.usefixtures('matches_tillPage1')
class TestTillPage1:

    def test_common(self, grabber: Grabber):
        assert grabber.leagueGrid.isVisibleSeasonTabs()
        assert grabber.leagueGrid.isLoadedGrid()
        assert not grabber.leagueGrid.isEndOfSeason()
        assert not grabber.leagueGrid.isEmpty()
        assert not grabber.leagueGrid.isReload()
        assert grabber.leagueGrid.isVisibleNavigationButtons()

    def test_matchesLength(self, matches_tillPage1):
        assert len(matches_tillPage1) == 50

    def test_SCL(self, grabber: Grabber):
        assert grabber.leagueGrid.getSCL() == ('Soccer', 'Argentina', 'Superliga')

    def test_currentSeasonName(self, grabber: Grabber):
        assert grabber.leagueGrid.getCurrentSeasonName() == '2017/2018'

    def test_seasons(self, grabber: Grabber):
        seasons = grabber.leagueGrid.getSeasonTabs()
        assert seasons[0].text == '2017/2018'

    def test_navigation(self, grabber: Grabber):
        btns = grabber.leagueGrid.getNavigationButtons()
        assert '1' not in btns
        assert '2' in btns


@pytest.mark.usefixtures('matches_tillPage3')
class TestTillPage3:

    def test_common(self, grabber: Grabber):
        assert not grabber.leagueGrid.isEndOfSeason()

    def test_matchesLength(self, matches_tillPage3):
        assert len(matches_tillPage3) == 150

    def test_navigation(self, grabber: Grabber):
        btns = grabber.leagueGrid.getNavigationButtons()
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
        assert match.date == '20180515'
        assert match.time == '03:15'
        assert match.teams == ['Gimnasia L.P.', 'Newells Old Boys']
        assert match.url == 'https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/gimnasia-l-p-newells-old-boys-QVBrfakT/'
        assert match.id == 'QVBrfakT'
        assert match.scoreString == '2:0'
        assert match.odds == {'1X2': {'1': 2.73, 'X': 3.05, '2': 2.75}}
        assert match.bkNum == 3
        assert match.finished

    def test_lastMatch(self, matches_tillPage3: List[Match]):
        match = matches_tillPage3[-1]

        assert match.season == '2017/2018'
        assert match.date == '20180225'
        assert match.time == '01:15'
        assert match.teams == ['Velez Sarsfield', 'River Plate']
        assert match.url == 'https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/velez-sarsfield-river-plate-xGt8WUHH/'
        assert match.id == 'xGt8WUHH'
        assert match.scoreString == '1:0'
        assert match.odds == {'1X2': {'1': 3.2, 'X': 3.22, '2': 2.35}}
        assert match.bkNum == 3
        assert match.finished


@pytest.mark.skip()
@pytest.mark.usefixtures('matches_tillLast')
class TestTillLast:

    def test_common(self, grabber: Grabber):
        assert grabber.leagueGrid.isEndOfSeason()
        assert grabber.leagueGrid.isEmpty()

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
        assert match.scoreString == '1:1'
        assert match.odds == {'1X2': {'1': 2.9, 'X': 2.2, '2': 3.66}}
        assert match.bkNum == 1
        assert match.finished
