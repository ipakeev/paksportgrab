import re
import time
import datetime
from functools import partial
from typing import Optional, Union, List, Tuple, Callable
from pakselenium import Browser
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException

from .oddsportal.user import User
from .oddsportal.sportGrid import SportGrid
from .oddsportal.leagueGrid import LeagueGrid
from .oddsportal.matchGrid import MatchGrid
from .oddsportal.units.league import League, SeasonDescribe
from .oddsportal.units.match import Match
from .oddsportal.config import names, GLOBAL
from .oddsportal import utils


def catchExceptions(func):
    def wrapper(self, *args, **kwargs):
        if GLOBAL.debug:
            return func(self, *args, **kwargs)

        crash = 0
        while 1:
            try:
                return func(self, *args, **kwargs)
            except StaleElementReferenceException:
                # when click was wrong
                pass
            except AssertionError:
                # when unknown error (tab name)
                print('>!> Assertion error')
                print(func, args, kwargs)
            except WebDriverException:
                # when browser is closed
                crash += 1
                if crash == 5:
                    print('>!> new session')
                    self.newBrowserSession()
                    crash = 0
            except Exception as e:
                print(func, args, kwargs)
                raise e
            time.sleep(1)

    return wrapper


class Grabber(object):
    browser: Browser
    user: User
    sportGrid: SportGrid
    leagueGrid: LeagueGrid
    matchGrid: MatchGrid

    def __init__(self, browser: Browser, cookiePath: str = None):
        self.browser = browser
        self.browser.go = partial(self.browser.go, isReachedUrl=utils.isReachedUrl)
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

    def go(self, url: str,
           until: Union[Callable, Tuple[Callable, ...]] = None,
           empty: Callable = None,
           reload: Callable = None):
        while 1:
            self.browser.go(url, until=until, empty=empty, reload=reload)
            if self.user.isLoggedIn():
                break
            else:
                self.user.login()

    @catchExceptions
    def getLeagues(self, sport: str, date: datetime.date) -> Optional[List[League]]:
        url = utils.getDateSportUrl(sport, date)

        self.go(url, until=self.sportGrid.isLoadedGrid,
                empty=self.sportGrid.isEmpty, reload=self.sportGrid.isReload)

        if self.sportGrid.isEmpty():
            return None

        self.sportGrid.switchToEvents()
        return self.sportGrid.grab()

    @catchExceptions
    def getSeasons(self, leagueUrl: str) -> List[SeasonDescribe]:
        self.go(leagueUrl, until=self.leagueGrid.isLoadedGrid,
                empty=self.leagueGrid.isEmpty, reload=self.leagueGrid.isReload)

        if self.leagueGrid.isVisibleSeasonTabs():
            seasons = self.leagueGrid.getSeasonTabs()
            return [SeasonDescribe(name=i.text, url=i.getAttribute('href')) for i in seasons]
        else:
            return []

    @catchExceptions
    def getMatches(self, leagueUrl: str, tillMatchId: str = None,
                   seasonsDepth: int = 5, seasonMin='2014') -> List[Match]:
        def isReachedSeason():
            if self.leagueGrid.isVisibleSeasonTabs():
                return self.leagueGrid.getCurrentSeasonName() == seasonName

        self.go(leagueUrl, until=self.leagueGrid.isLoadedGrid,
                empty=self.leagueGrid.isEmpty, reload=self.leagueGrid.isReload)

        matches = []

        if self.leagueGrid.isEmpty():
            return matches

        seasonElements = self.leagueGrid.getSeasonTabs()
        seasonsUrls = {i.text: i.getAttribute('href') for i in seasonElements}
        seasonNames = [i.text for i in seasonElements]  # new list because needs course of seasons
        start = [i.getAttribute('href') for i in seasonElements].index(leagueUrl)
        assert start < seasonsDepth
        seasonNames = seasonNames[start:seasonsDepth]

        for seasonName in seasonNames:
            if re.findall(r'(\d{4})', seasonName)[0] < seasonMin:
                continue
            url = seasonsUrls[seasonName]
            if not isReachedSeason():
                self.go(url, until=(self.leagueGrid.isLoadedGrid, isReachedSeason),
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
            seasonsUrls = {i.text: i.getAttribute('href') for i in seasonElements}

        return matches

    @catchExceptions
    def fillMatch(self, match: Match, fillFinished=False):
        if match.filledScore and match.filledOdds:
            return
        oddsTabs = names.sportTabs[match.sport]

        def getTabsNameList():
            current = self.matchGrid.getCurrentTabName()
            tabsNameList = list(oddsTabs.keys())
            if current in tabsNameList:
                return [current] + [i for i in tabsNameList if (i != current and i in tabs)]
            else:
                return [i for i in tabsNameList if i in tabs]

        def getSubTabsNameList():
            current = self.matchGrid.getCurrentSubTabName()
            subTabsNameList = oddsTabs[tabName]
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

        match.updatedAt = datetime.datetime.today()
        match.dateTime = self.matchGrid.getDateTime()
        match.scoreString = self.matchGrid.getResult()
        match.score = None

        if match.scoreString:
            match.setFinished()
            match.filledScore = True

        if fillFinished and not match.finished:
            return

        if match.filledOdds:
            return

        for tabName in oddsTabs.keys():
            match.odds[tabName] = {subTabName: None for subTabName in oddsTabs[tabName]}

        if self.matchGrid.isEmpty():
            match.filledOdds = True
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

        match.filledOdds = True

    def testMatch(self, sport: str, url: str):
        oddsTabs = names.sportTabs[sport]

        def getTabsNameList():
            current = self.matchGrid.getCurrentTabName()
            tabsNameList = list(oddsTabs.keys())
            if current in tabsNameList:
                return [current] + [i for i in tabsNameList if (i != current and i in tabs)]
            else:
                return [i for i in tabsNameList if i in tabs]

        def getSubTabsNameList():
            current = self.matchGrid.getCurrentSubTabName()
            subTabsNameList = oddsTabs[tabName]
            if current in subTabsNameList:
                return [current] + [i for i in subTabsNameList if (i != current and i in subTabs)]
            else:
                return [i for i in subTabsNameList if i in subTabs]

        def isReachedTab():
            return self.matchGrid.getCurrentTabName() == tabName

        def isReachedSubTab():
            return self.matchGrid.getCurrentSubTabName() == subTabName

        print(f'isReachedUrl: {utils.isReachedUrl(url)(self.browser.browser)}')
        print(f'target: {url}, current: {self.browser.currentUrl}')

        print(f'isLoadedGrid: {self.matchGrid.isLoadedGrid()}')
        print(f'isEmpty: {self.matchGrid.isEmpty()}')
        print(f'isReload: {self.matchGrid.isReload()}')

        odds = {}
        for tabName in oddsTabs.keys():
            odds[tabName] = {subTabName: None for subTabName in oddsTabs[tabName]}

        tabs = self.matchGrid.getTabs()
        print(f'tabs: {tabs.keys()}')
        for tabName in getTabsNameList():
            print(f'> tab: {tabName}')
            if not isReachedTab():
                print(f'click on {tabName}')
                self.browser.click(tabs[tabName],
                                   until=(self.matchGrid.isLoadedGrid, isReachedTab),
                                   reload=self.matchGrid.isReload)
                print(f'res: [{self.matchGrid.isLoadedGrid()}, {isReachedTab()}], [{self.matchGrid.isReload()}')

            subTabs = self.matchGrid.getSubTabs()
            print(f'subTabs: {subTabs}')
            for subTabName in getSubTabsNameList():
                print(f'> subTab: {subTabName}')
                if not isReachedSubTab():
                    print(f'click on {subTabName}')
                    self.browser.click(subTabs[subTabName],
                                       until=(self.matchGrid.isLoadedGrid, isReachedSubTab),
                                       reload=self.matchGrid.isReload)
                    print(f'res: [{self.matchGrid.isLoadedGrid()}, {isReachedSubTab()}], [{self.matchGrid.isReload()}')

                print(self.matchGrid.grab(tabName))
