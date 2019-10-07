import pytest
from paksportgrab.grabber import Grabber
from paksportgrab.oddsportal.config import names


class Match:
    date: str
    time: str
    score: str
    leagueUrl: str
    odds: dict

    def __init__(self, url):
        self.url = url
        self.odds = {}


@pytest.fixture(scope='module', autouse=True)
def match(grabber: Grabber):
    url = 'https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/tigre-patronato-pCQq96qD/'
    m = Match(url)
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

    score = '1:3 (1:1, 0:2)'
    assert grabber.matchGrid.getResult() == score
    assert match.score == score


def test_grid(match: Match):
    assert match.odds[names.WDL][names.ft] == {'1': 1.79, 'X': 3.52, '2': 4.85, 'bkNum': 3}
    assert match.odds[names.WDL][names.h1] == {'1': 2.43, 'X': 2.11, '2': 5.43, 'bkNum': 3}

    assert match.odds[names.handicap][names.ft][0] == {'1': 1.3, '2': 3.43, 'bkNum': 3}
    assert match.odds[names.handicap][names.h1][-0.5] == {'1': 2.3, '2': 1.48, 'bkNum': 1}

    assert len(match.odds[names.handicap][names.ft]) == 12
    assert len(match.odds[names.handicap][names.h1]) == 5

    assert match.odds[names.total][names.ft][2.5] == {'over': 2.25, 'under': 1.67, 'bkNum': 3}
    assert match.odds[names.total][names.h1][1] == {'over': 2.08, 'under': 1.75, 'bkNum': 1}

    assert len(match.odds[names.total][names.ft]) == 11
    assert len(match.odds[names.total][names.h1]) == 5
