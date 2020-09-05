import datetime

import pytest

from paksportgrab.grabber import Grabber
from paksportgrab.oddsportal.config import names
from paksportgrab.oddsportal.units.match import Match


@pytest.fixture(scope='module', autouse=True)
def match(grabber: Grabber):
    m = Match()
    m.sport = 'soccer'
    m.url = 'https://www.oddsportal.com/soccer/argentina/superliga-2017-2018/tigre-patronato-pCQq96qD/'
    m.odds = {}
    m.set_finished()
    m.filled_score = False
    m.filled_odds = False
    grabber.fill_match(m)
    return m


def test_common(grabber: Grabber):
    assert grabber.match_grid.is_loaded_grid()
    assert grabber.match_grid.is_visible_tabs()
    assert grabber.match_grid.is_visible_sub_tabs()
    assert not grabber.match_grid.is_empty()
    assert not grabber.match_grid.is_reload()


def test_tabs(grabber: Grabber):
    assert grabber.match_grid.get_current_tab_name() in names.tab_name.values()
    tabs = grabber.match_grid.get_tabs()
    assert names.tab.WDL in tabs
    assert names.tab.handicap in tabs
    assert names.tab.total in tabs
    assert names.tab.WL not in tabs


def test_subTabs(grabber: Grabber):
    assert grabber.match_grid.get_current_sub_tab_name() in names.sub_tab_name.values()
    subTabs = grabber.match_grid.get_sub_tabs()
    assert names.sub_tab.ft in subTabs
    assert names.sub_tab.ftot not in subTabs
    assert names.sub_tab.h1 in subTabs
    assert names.sub_tab.q1 not in subTabs


def test_text(grabber: Grabber, match: Match):
    assert grabber.match_grid.get_SCL() == ('Soccer', 'Argentina', 'Superliga 2017/2018')
    assert grabber.match_grid.get_teams() == ['Tigre', 'Patronato']

    dt = datetime.datetime(2017, 9, 16, 1, 5)
    assert grabber.match_grid.get_date_time() == dt
    assert match.date == dt.date()
    assert match.time == dt.time()

    scoreString = '1:3 (1:1, 0:2)'
    assert grabber.match_grid.get_result() == scoreString
    assert grabber.match_grid.is_finished()
    assert match.score_string == scoreString


def test_grid(match: Match):
    odds = match.odds[names.tab.WDL][names.sub_tab.ft]
    assert 1.6 <= odds['1'] <= 2.0
    assert 3.3 <= odds['X'] <= 3.6
    assert 4.5 <= odds['2'] <= 4.9
    assert 9 <= odds['bk_num'] <= 15

    odds = match.odds[names.tab.WDL][names.sub_tab.h1]
    assert 2.25 <= odds['1'] <= 2.6
    assert 1.9 <= odds['X'] <= 2.25
    assert 4.8 <= odds['2'] <= 5.3
    assert 6 <= odds['bk_num'] <= 12

    odds = match.odds[names.tab.handicap][names.sub_tab.ft][0]
    assert 1.2 <= odds['1'] <= 1.45
    assert 3.2 <= odds['2'] <= 3.7
    assert 4 <= odds['bk_num'] <= 8
    assert 15 <= len(match.odds[names.tab.handicap][names.sub_tab.ft]) <= 20

    odds = match.odds[names.tab.total][names.sub_tab.ft][2.5]
    assert 2.1 <= odds['over'] <= 2.4
    assert 1.55 <= odds['under'] <= 1.8
    assert 8 <= odds['bk_num'] <= 12

    odds = match.odds[names.tab.total][names.sub_tab.h1][1]
    assert 2.05 <= odds['over'] <= 2.3
    assert 1.6 <= odds['under'] <= 1.85
    assert 2 <= odds['bk_num'] <= 5

    assert 10 <= len(match.odds[names.tab.total][names.sub_tab.ft]) <= 15
    assert 4 <= len(match.odds[names.tab.total][names.sub_tab.h1]) <= 8
