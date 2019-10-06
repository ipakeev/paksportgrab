from typing import Dict, Optional
from pakselenium.browser import Browser, PageElement

from .border import Border
from .. import utils
from ..config import names


class Match(object):
    url: str
    id: str
    sport: str
    country: str
    league: str
    season: str
    countryId: int
    leagueId: int
    teams: list
    score: Optional[str]
    date: str
    time: str
    odds: Dict[str, Dict[str, dict]]
    bkNum: Optional[int]
    notStarted: bool
    live: bool
    finished: bool
    canceled: bool
    filledOdds: bool
    filledScore: bool

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

    def __init__(self, browser: Browser, border: Border, pe: PageElement):
        self.date = border.date

        time = browser.findElementFrom(pe, 'td.table-time')
        self.time = time.text

        teams = browser.findElementFrom(pe, 'td.name')
        self.teams = teams.text.split(' - ')
        url = browser.findElementsFrom(teams, 'a')
        url = [i.getAttribute('href') for i in url]
        if len(url) == 1:
            self.url = url[0]
        else:
            url = [i for i in url if (i.startswith('https://') and 'inplay-odds' not in i)]
            assert len(url) == 1
            self.url = url[0]
        self.id = utils.getMatchId(self.url)

        score = browser.findElementsFrom(pe, 'td.table-score')
        if score:
            assert len(score) == 1
            score = score[0]
            self.score = score.text
            if self.score in names.cancelledTypes:
                self.setCanceled()
            elif 'live-score' in score.getAttribute('class'):
                self.setLive()
            else:
                self.setFinished()
        else:
            self.score = None
            self.setNotStarted()

        odds = browser.findElementsFrom(pe, 'td.odds-nowrp')
        odds = [i.text for i in odds]
        odds = [float(i) if i != '-' else None for i in odds]
        assert len(odds) == len(border.oddsType)
        odds = {t: odd for t, odd in zip(border.oddsType, odds)}
        self.odds = {
            '1X2': odds,
        }

        bkNum = browser.findElementFrom(pe, 'td.info-value')
        try:
            self.bkNum = int(bkNum.text)
        except ValueError:
            self.bkNum = None

        self.filledOdds = False
        self.filledScore = False
