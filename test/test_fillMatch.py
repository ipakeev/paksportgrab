import pytest
from paksportgrab.grabber import Grabber
from paksportgrab.oddsportal.config import names


class Match:
    sport: str
    date: str
    time: str
    scoreString: str
    odds: dict
    finished: bool = True
    filledScore: bool = False
    filledOdds: bool = False

    def __init__(self, sport, url):
        self.sport = sport
        self.url = url
        self.odds = dict()


@pytest.fixture(scope='module', autouse=True)
def match(grabber: Grabber):
    sport = 'soccer'
    url = 'https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/tigre-patronato-pCQq96qD/'
    m = Match(sport, url)
    grabber.fillMatch(m)
    return m


def test_common(grabber: Grabber):
    assert grabber.matchGrid.isLoadedGrid()
    assert grabber.matchGrid.isVisibleTabs()
    assert grabber.matchGrid.isVisibleSubTabs()
    assert not grabber.matchGrid.isEmpty()
    assert not grabber.matchGrid.isReload()


def test_tabs(grabber: Grabber):
    assert grabber.matchGrid.getCurrentTabName() in names.tabName.values()
    tabs = grabber.matchGrid.getTabs()
    assert names.WDL in tabs
    assert names.handicap in tabs
    assert names.total in tabs
    assert names.WL not in tabs


def test_subTabs(grabber: Grabber):
    assert grabber.matchGrid.getCurrentSubTabName() in names.subTabName.values()
    subTabs = grabber.matchGrid.getSubTabs()
    assert names.ft in subTabs
    assert names.ftot not in subTabs
    assert names.h1 in subTabs
    assert names.q1 not in subTabs


def test_text(grabber: Grabber, match: Match):
    assert grabber.matchGrid.getSCL() == ('Soccer', 'Argentina', 'Superliga 2017/2018')
    assert grabber.matchGrid.getTeams() == ['Tigre', 'Patronato']

    date, time = '20170916', '01:05'
    assert grabber.matchGrid.getDateTime() == (date, time)
    assert match.date == date
    assert match.time == time

    scoreString = '1:3 (1:1, 0:2)'
    assert grabber.matchGrid.getResult() == scoreString
    assert grabber.matchGrid.isFinished()
    assert match.scoreString == scoreString


def test_grid(match: Match):
    assert match.odds[names.WDL][names.ft] == {'1': 1.78, 'X': 3.44, '2': 4.7, 'bkNum': 14}
    assert match.odds[names.WDL][names.h1] == {'1': 2.42, 'X': 2.04, '2': 5.04, 'bkNum': 11}

    assert match.odds[names.handicap][names.ft][0] == {'1': 1.3, '2': 3.53, 'bkNum': 7}
    assert len(match.odds[names.handicap][names.ft]) == 18

    assert match.odds[names.total][names.ft][2.5] == {'over': 2.22, 'under': 1.65, 'bkNum': 12}
    assert match.odds[names.total][names.h1][1] == {'over': 2.18, 'under': 1.68, 'bkNum': 4}

    assert len(match.odds[names.total][names.ft]) == 13
    assert len(match.odds[names.total][names.h1]) == 7
