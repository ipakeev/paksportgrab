import datetime
from copy import deepcopy
from typing import List, Dict, Optional, Union

from pakselenium import Browser, PageElement, Selector, By

from .border import Border
from .. import utils
from ..config import names


class Match:
    url: str
    id: str
    sport: str
    country: str
    league: str
    league_id: int
    season: str
    teams: list
    score_string: Optional[str]
    score: Optional[dict]
    date: datetime.date
    time: Union[datetime.time, str]
    _date_time: datetime.datetime
    odds: Dict[str, Dict[str, dict]]
    bk_num: Optional[int]
    not_started: bool
    live: bool
    finished: bool
    canceled: bool
    filled_odds: bool
    filled_score: bool

    created_at: datetime.datetime
    updated_at: datetime.datetime
    made_next_at: datetime.datetime
    made_ready_at: datetime.datetime

    data: dict
    wdl_name: str
    score_name: str
    tot_bk: float
    hp_bk: float

    @property
    def date_time(self):
        return self._date_time

    @date_time.setter
    def date_time(self, dt: datetime.datetime):
        self._date_time = dt
        self.date = dt.date()
        self.time = dt.time()

    def set_not_started(self):
        self.not_started = True
        self.live = False
        self.finished = False
        self.canceled = False

    def set_live(self):
        self.not_started = False
        self.live = True
        self.finished = False
        self.canceled = False

    def set_finished(self):
        self.not_started = False
        self.live = False
        self.finished = True
        self.canceled = False

    def set_canceled(self):
        self.not_started = False
        self.live = False
        self.finished = False
        self.canceled = True

    def to_dict(self):
        return self.__dict__

    def load(self, attrs: dict):
        self.__dict__.update(attrs)
        return self

    def get_odds(self, tab: str, value: Union[str, float] = None) -> Optional[List[float]]:
        if tab not in self.odds:
            return None

        loc = self.odds[tab][self.score_name]
        if not loc:
            return None

        if tab == names.tab.WDL:
            return [loc['1'], loc['X'], loc['2']]

        elif tab == names.tab.WL:
            return [loc['1'], loc['2']]

        elif tab == names.tab.total:
            if value is None or value == 'bk':
                value = self.tot_bk
            if value not in loc:
                return None
            loc = loc[value]
            return [loc['over'], loc['under']]

        elif tab == names.tab.handicap:
            if value is None or value == 'bk':
                value = self.hp_bk
            if value not in loc:
                return None
            loc = loc[value]
            return [loc['1'], loc['2']]

        else:
            print(tab)
            raise ValueError(tab)

    def copy(self):
        return deepcopy(self)

    def parse(self, browser: Browser, border: Border, pe: PageElement):
        self.date = border.date

        time = browser.find_element_from(pe, Selector(By.CSS_SELECTOR, 'td.table-time'))
        try:
            self.time = datetime.time.fromisoformat(time.text)
            self.date_time = datetime.datetime.combine(self.date, self.time)
        except ValueError:
            self.time = time.text

        teams = browser.find_element_from(pe, Selector(By.CSS_SELECTOR, 'td.name'))
        self.teams = teams.text.split(' - ')
        url = browser.find_elements_from(teams, Selector(By.CSS_SELECTOR, 'a'))
        url = [i.get_attribute('href') for i in url]
        if len(url) == 1:
            self.url = url[0]
        else:
            url = [i for i in url if (i.startswith('https://') and 'inplay-odds' not in i)]
            assert len(url) == 1
            self.url = url[0]
        self.id = utils.get_match_id(self.url)

        scoreString = browser.find_elements_from(pe, Selector(By.CSS_SELECTOR, 'td.table-score'))
        if scoreString:
            assert len(scoreString) == 1
            scoreString = scoreString[0]
            self.score_string = scoreString.text
            if self.score_string in names.cancelled_types:
                self.set_canceled()
            elif 'live-score' in scoreString.get_attribute('class') or 'live-score' in time.get_attribute('class'):
                self.set_live()
            else:
                self.set_finished()
                assert self.date_time
        else:
            self.score_string = None
            self.set_not_started()
        self.score = None

        # odds = browser.find_elements_from(pe, 'td.odds-nowrp')
        # odds = [i.text for i in odds]
        # odds = [float(i) if i != '-' else None for i in odds]
        # assert len(odds) == len(border.odds_type)
        # odds = {t: odd for t, odd in zip(border.odds_type, odds)}
        # self.odds = {
        #     names.WDL: odds,
        # }
        self.odds = {}

        bkNum = browser.find_element_from(pe, Selector(By.CSS_SELECTOR, 'td.info-value'))
        try:
            self.bk_num = int(bkNum.text)
        except ValueError:
            self.bk_num = None

        self.filled_odds = False
        self.filled_score = False

        return self
