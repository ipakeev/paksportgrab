import time
import collections
from typing import Optional, Union, List, Tuple, Callable
from pakselenium import Browser
from selenium.common.exceptions import WebDriverException

from .oddsportal.user import User
from .oddsportal.sportGrid import SportGrid
from .oddsportal.leagueGrid import LeagueGrid
from .oddsportal.matchGrid import MatchGrid
from .oddsportal.units.league import League
from .oddsportal.units.match import Match
from .oddsportal.config import names
from .oddsportal import utils


def catchWebDriverException(func):
    def wrapper(self, *args, **kwargs):
        while 1:
            try:
                return func(self, *args, **kwargs)
            except WebDriverException:
                # when browser is closed
                self.newBrowserSession()
            except Exception as e:
                print(func, args, kwargs)
                raise e
            time.sleep(1)

    return wrapper


SeasonDescribe = collections.namedtuple('SeasonDescribe', ['name', 'url'])


class Grabber(object):
    browser: Browser
    user: User
    sportGrid: SportGrid
    leagueGrid: LeagueGrid
    matchGrid: MatchGrid

    def __init__(self, browser: Browser, cookiePath: str = None):
        self.browser = browser
        self.user = User(self.browser)
        self.sportGrid = SportGrid(self.browser)
        self.leagueGrid = LeagueGrid(self.browser)
        self.matchGrid = MatchGrid(self.browser)

        if cookiePath is not None:
            names.cookiePath = cookiePath

    def newBrowserSession(self):
        self.browser.newSession()
        self.user.login()

    def login(self, username: str, password: str):
        self.user.setLoginData(username, password)
        self.user.login()

    def go(self, url: str, until: Union[Callable, Tuple[Callable, ...]] = None,
           empty: Callable = None, reload: Callable = None):
        while 1:
            self.browser.go(url, until=until, empty=empty, reload=reload)
            if self.user.isLoggedIn():
                break
            self.user.login()

    @catchWebDriverException
    def getLeagues(self, sport: str, date: str) -> Optional[List[League]]:
        url = utils.getDateSportUrl(sport, date)

        self.go(url, until=self.sportGrid.isLoadedGrid,
                empty=self.sportGrid.isEmpty, reload=self.sportGrid.isReload)

        if self.sportGrid.isEmpty():
            return None

        self.sportGrid.switchToEvents()
        return self.sportGrid.grab()

    @catchWebDriverException
    def getSeasons(self, leagueUrl: str) -> List[SeasonDescribe]:
        self.go(leagueUrl, until=self.leagueGrid.isLoadedGrid,
                empty=self.leagueGrid.isEmpty, reload=self.leagueGrid.isReload)

        if self.leagueGrid.isVisibleSeasonTabs():
            seasons = self.leagueGrid.getSeasonTabs()
            return [SeasonDescribe(name=i.text, url=i.getAttribute('href')) for i in seasons]
        else:
            return []

    @catchWebDriverException
    def getMatches(self, leagueUrl: str, tillMatchId: str = None) -> List[Match]:
        def isReachedSeason():
            if self.leagueGrid.isVisibleSeasonTabs():
                return self.leagueGrid.getCurrentSeasonName() == seasonName

        self.go(leagueUrl, until=self.leagueGrid.isLoadedGrid,
                empty=self.leagueGrid.isEmpty, reload=self.leagueGrid.isReload)

        matches = []

        if self.leagueGrid.isEmpty():
            return matches

        seasonElements = self.leagueGrid.getSeasonTabs()
        seasonsDict = {i.text: i for i in seasonElements}
        seasonNames = [i.text for i in seasonElements]  # new list because needs course of seasons
        startFrom = [i.getAttribute('href') for i in seasonElements].index(leagueUrl)
        for seasonName in seasonNames[startFrom:]:
            season = seasonsDict[seasonName]
            if not isReachedSeason():
                self.browser.click(season, until=(self.leagueGrid.isLoadedGrid, isReachedSeason),
                                   empty=self.leagueGrid.isEmpty, reload=self.leagueGrid.isReload)

            if not self.leagueGrid.isEmpty():
                while 1:
                    new = self.leagueGrid.grab()
                    for m in new:
                        m.season = seasonName
                    matches.extend(new)

                    if tillMatchId:
                        if tillMatchId in [i.id for i in new]:
                            return matches

                    if self.leagueGrid.isEndOfSeason():
                        break
                    self.leagueGrid.nextPage()

            seasonElements = self.leagueGrid.getSeasonTabs()
            seasonsDict = {i.text: i for i in seasonElements}

        return matches

    @catchWebDriverException
    def fillMatch(self, match: Match):
        def getTabsNameList():
            current = self.matchGrid.getCurrentTabName()
            if current in names.tabs:
                return [current] + [i for i in names.tabs if (i != current and i in tabs)]
            else:
                return [i for i in names.tabs if i in tabs]

        def getSubTabsNameList():
            current = self.matchGrid.getCurrentSubTabName()
            subTabsNameList = names.subTabs[tabName]
            if current in subTabsNameList:
                return [current] + [i for i in subTabsNameList if (i != current and i in subTabs)]
            else:
                return [i for i in subTabsNameList if i in subTabs]

        def isReachedTab():
            return self.matchGrid.getCurrentTabName() == tabName

        def isReachedSubTab():
            return self.matchGrid.getCurrentSubTabName() == subTabName

        self.go(match.url, until=self.matchGrid.isLoadedGrid,
                empty=self.matchGrid.isEmpty, reload=self.matchGrid.isReload)

        match.date, match.time = self.matchGrid.getDateTime()
        match.score = self.matchGrid.getResult()
        for tabName in names.tabs:
            match.odds[tabName] = {key: None for key in names.subTabs[tabName]}

        if self.matchGrid.isEmpty():
            return

        tabs = self.matchGrid.getTabs()
        for tabName in getTabsNameList():
            if not isReachedTab():
                self.browser.click(tabs[tabName],
                                   until=(self.matchGrid.isLoadedGrid, isReachedTab),
                                   reload=self.matchGrid.isReload)

            subTabs = self.matchGrid.getSubTabs()
            for subTabName in getSubTabsNameList():
                if not isReachedSubTab():
                    self.browser.click(subTabs[subTabName],
                                       until=(self.matchGrid.isLoadedGrid, isReachedSubTab),
                                       reload=self.matchGrid.isReload)

                match.odds[tabName][subTabName] = self.matchGrid.grab(tabName)
