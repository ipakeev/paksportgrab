from typing import Tuple, List, Dict
from pakselenium import Browser
from pakselenium.browser import PageElement

from .config.selector import leaguePage
from .grid import Grid
from .units.border import LeagueGridBorder
from .units.match import Match


def catchExceptions(func):
    def wrapper(self, *args, **kwargs):
        while 1:
            try:
                return func(self, *args, **kwargs)
            except ValueError:
                self.browser.refresh(until=self.isLoadedGrid)
            except Exception as e:
                if self.isReload():
                    self.browser.refresh(until=self.isLoadedGrid)
                    continue
                print('msg: {}'.format(self.msg))
                raise e

    return wrapper


class LeagueGrid(Grid):
    browser: Browser

    def __init__(self, browser: Browser):
        super().__init__()
        self.browser = browser

    def getSCL(self) -> Tuple[str, str, str]:
        # ['/', sport, country, league]
        pes = self.browser.findElements(leaguePage.SCL)
        _, sport, country, league = [i.text for i in pes]
        league = league.replace(self.getCurrentSeasonName(), '').strip()
        return sport, country, league

    def getNavigationButtons(self) -> Dict[str, PageElement]:
        pes = self.browser.findElements(leaguePage.navigation.buttons)
        buttons = {i.text: i for i in pes}
        return buttons

    def getCurrentSeasonName(self) -> str:
        # ['RESULTS', current season]
        pes = self.browser.findElements(leaguePage.navigation.currentSeason)
        tab, season = [i.text for i in pes]
        assert tab == 'RESULTS'
        return season

    def getSeasonTabs(self) -> List[PageElement]:
        # ['NEXT MATCHES', 'RESULTS', 'STANDINGS', 'OUTRIGHTS', list of seasons]
        pes = self.browser.findElements(leaguePage.navigation.seasons)
        seasons = [i for i in pes if i.text not in leaguePage.ignoreTabs]

        # sort seasons, first current season
        current = self.getCurrentSeasonName()
        index = [n for n, i in enumerate(seasons) if i.text == current][0]
        current = seasons.pop(index)

        return [current] + seasons

    @catchExceptions
    def grab(self) -> List[Match]:
        border = LeagueGridBorder()
        matches = []
        for row in self.browser.findElements(leaguePage.grid):
            cl = row.getAttribute('class')
            if 'deactivate' in cl:  # матч
                m = Match().parse(self.browser, border, row)
                if m.bkNum is None:
                    print('>!> invalid bk odds: {}'.format(self.browser.currentUrl))
                    raise ValueError
                if m.finished:
                    matches.append(m)
            elif 'nob-border' in cl:  # дата
                border.update(self.browser, row)
            elif 'dark center' in cl:  # шапка
                continue
            elif 'table-dummyrow' in cl:  # пустая строка
                continue
            else:
                raise StopIteration(cl)
        return matches

    def nextPage(self):
        def isGotNext():
            if self.browser.isOnPage(leaguePage.navigation.buttons):
                return current in self.getNavigationButtons()

        current = self.browser.findElement(leaguePage.navigation.currentPage).text
        buttons = self.getNavigationButtons()
        self.browser.click(buttons[leaguePage.navigation.nextButton], until=(self.isLoadedGrid, isGotNext))

    def isEndOfSeason(self) -> bool:
        if not self.isVisibleNavigationButtons():
            return True

        buttons = self.getNavigationButtons()
        urls = {key: pe.getAttribute('href') for key, pe in buttons.items()}
        if urls[leaguePage.navigation.nextButton] == urls[leaguePage.navigation.endButton]:
            if list(urls.values()).count(urls[leaguePage.navigation.endButton]) == 2:
                return True

    def isLoadedGrid(self) -> bool:
        return self.browser.isOnPage(leaguePage.gridElement)

    def isVisibleNavigationButtons(self) -> bool:
        return self.browser.isOnPage(leaguePage.navigation.buttons)

    def isVisibleSeasonTabs(self) -> bool:
        return self.browser.isOnPage(leaguePage.navigation.seasons)
