import datetime
from typing import List, Dict, Optional, Union
from copy import deepcopy
from pakselenium.browser import Browser, PageElement
from selenium.webdriver.common.by import By

from .border import Border
from .. import utils
from ..config import names


class Match:
    url: str
    id: str
    sport: str
    country: str
    league: str
    leagueId: int
    season: str
    teams: list
    scoreString: Optional[str]
    score: Optional[dict]
    date: datetime.date
    time: Union[datetime.time, str]
    _dateTime: datetime.datetime
    odds: Dict[str, Dict[str, dict]]
    bkNum: Optional[int]
    notStarted: bool
    live: bool
    finished: bool
    canceled: bool
    filledOdds: bool
    filledScore: bool

    data: dict
    wdlName: str
    scoreName: str
    totBk: float
    hpBk: float

    @property
    def dateTime(self):
        return self._dateTime

    @dateTime.setter
    def dateTime(self, dt: datetime.datetime):
        self._dateTime = dt
        self.date = dt.date()
        self.time = dt.time()

    def setNotStarted(self):
        self.notStarted = True
        self.live = False
        self.finished = False
        self.canceled = False

    def setLive(self):
        self.notStarted = False
        self.live = True
        self.finished = False
        self.canceled = False

    def setFinished(self):
        self.notStarted = False
        self.live = False
        self.finished = True
        self.canceled = False

    def setCanceled(self):
        self.notStarted = False
        self.live = False
        self.finished = False
        self.canceled = True

    def toDict(self):
        d = {}
        for name in self.__dir__():
            attr = self.__getattribute__(name)
            if name.startswith('_') or callable(attr):
                continue
            d[name] = attr
        return d

    def load(self, attrs: dict):
        for name, value in attrs.items():
            self.__setattr__(name, value)
        return self

    def getOdds(self, tab: str) -> Optional[List[float]]:
        if tab == names.tab.WDL:
            loc = self.odds[tab][self.scoreName]
            if not loc:
                return None
            return [loc['1'], loc['X'], loc['2']]

        elif tab == names.tab.WL:
            loc = self.odds[tab][self.scoreName]
            if not loc:
                return None
            return [loc['1'], loc['2']]

        elif tab == names.tab.total:
            loc = self.odds[tab][self.scoreName][self.totBk]
            return [loc['over'], loc['under']]

        elif tab == names.tab.handicap:
            loc = self.odds[tab][self.scoreName][self.hpBk]
            return [loc['1'], loc['2']]

        else:
            print(tab)
            raise ValueError(tab)

    def copy(self):
        return deepcopy(self)

    def parse(self, browser: Browser, border: Border, pe: PageElement):
        self.date = border.date

        time = browser.findElementFrom(pe, (By.CSS_SELECTOR, 'td.table-time'))
        try:
            self.time = datetime.time.fromisoformat(time.text)
        except ValueError:
            self.time = time.text

        teams = browser.findElementFrom(pe, (By.CSS_SELECTOR, 'td.name'))
        self.teams = teams.text.split(' - ')
        url = browser.findElementsFrom(teams, (By.CSS_SELECTOR, 'a'))
        url = [i.getAttribute('href') for i in url]
        if len(url) == 1:
            self.url = url[0]
        else:
            url = [i for i in url if (i.startswith('https://') and 'inplay-odds' not in i)]
            assert len(url) == 1
            self.url = url[0]
        self.id = utils.getMatchId(self.url)

        scoreString = browser.findElementsFrom(pe, (By.CSS_SELECTOR, 'td.table-score'))
        if scoreString:
            assert len(scoreString) == 1
            scoreString = scoreString[0]
            self.scoreString = scoreString.text
            if self.scoreString in names.cancelledTypes:
                self.setCanceled()
            elif 'live-score' in scoreString.getAttribute('class'):
                self.setLive()
            else:
                self.setFinished()
        else:
            self.scoreString = None
            self.setNotStarted()
        self.score = None

        # odds = browser.findElementsFrom(pe, 'td.odds-nowrp')
        # odds = [i.text for i in odds]
        # odds = [float(i) if i != '-' else None for i in odds]
        # assert len(odds) == len(border.oddsType)
        # odds = {t: odd for t, odd in zip(border.oddsType, odds)}
        # self.odds = {
        #     names.WDL: odds,
        # }
        self.odds = {}

        bkNum = browser.findElementFrom(pe, (By.CSS_SELECTOR, 'td.info-value'))
        try:
            self.bkNum = int(bkNum.text)
        except ValueError:
            self.bkNum = None

        self.filledOdds = False
        self.filledScore = False

        return self
