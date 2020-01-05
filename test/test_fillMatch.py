import pytest
import datetime
from paksportgrab.grabber import Grabber
from paksportgrab.oddsportal.units.match import Match
from paksportgrab.oddsportal.config import names


@pytest.fixture(scope='module', autouse=True)
def match(grabber: Grabber):
    m = Match()
    m.sport = 'soccer'
    m.url = 'https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/tigre-patronato-pCQq96qD/'
    m.odds = {}
    m.setFinished()
    m.filledScore = False
    m.filledOdds = False
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
    assert names.tab.WDL in tabs
    assert names.tab.handicap in tabs
    assert names.tab.total in tabs
    assert names.tab.WL not in tabs


def test_subTabs(grabber: Grabber):
    assert grabber.matchGrid.getCurrentSubTabName() in names.subTabName.values()
    subTabs = grabber.matchGrid.getSubTabs()
    assert names.subTab.ft in subTabs
    assert names.subTab.ftot not in subTabs
    assert names.subTab.h1 in subTabs
    assert names.subTab.q1 not in subTabs


def test_text(grabber: Grabber, match: Match):
    assert grabber.matchGrid.getSCL() == ('Soccer', 'Argentina', 'Superliga 2017/2018')
    assert grabber.matchGrid.getTeams() == ['Tigre', 'Patronato']

    dt = datetime.datetime(2017, 9, 16, 1, 5)
    assert grabber.matchGrid.getDateTime() == dt
    assert match.date == dt.date()
    assert match.time == dt.time()

    scoreString = '1:3 (1:1, 0:2)'
    assert grabber.matchGrid.getResult() == scoreString
    assert grabber.matchGrid.isFinished()
    assert match.scoreString == scoreString


def test_grid(match: Match):
    assert match.odds[names.tab.WDL][names.subTab.ft] == {'1': 1.78, 'X': 3.42, '2': 4.68, 'bkNum': 13}
    assert match.odds[names.tab.WDL][names.subTab.h1] == {'1': 2.42, 'X': 2.04, '2': 4.99, 'bkNum': 10}

    assert match.odds[names.tab.handicap][names.subTab.ft][0] == {'1': 1.31, '2': 3.52, 'bkNum': 6}
    assert len(match.odds[names.tab.handicap][names.subTab.ft]) == 18

    assert match.odds[names.tab.total][names.subTab.ft][2.5] == {'over': 2.22, 'under': 1.64, 'bkNum': 11}
    assert match.odds[names.tab.total][names.subTab.h1][1] == {'over': 2.21, 'under': 1.66, 'bkNum': 3}

    assert len(match.odds[names.tab.total][names.subTab.ft]) == 13
    assert len(match.odds[names.tab.total][names.subTab.h1]) == 7
