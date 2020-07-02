from typing import Tuple, List, Dict

from pakselenium import Browser, PageElement

from .config import GLOBAL
from .config.selector import leaguePage
from .grid import Grid
from .units.border import LeagueGridBorder
from .units.match import Match


def catchExceptions(func):
    def wrapper(self, *args, **kwargs):
        if GLOBAL.debug:
            return func(self, *args, **kwargs)

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
        pes = self.browser.find_elements(leaguePage.SCL)
        _, sport, country, league = [i.text for i in pes]
        league = league.replace(self.getCurrentSeasonName(), '').strip()
        return sport, country, league

    def getNavigationButtons(self) -> Dict[str, PageElement]:
        pes = self.browser.find_elements(leaguePage.navigation.buttons)
        buttons = {i.text: i for i in pes}
        return buttons

    def getCurrentSeasonName(self) -> str:
        # ['RESULTS', current season]
        pes = self.browser.find_elements(leaguePage.navigation.currentSeason)
        tab, season = [i.text for i in pes]
        assert tab == 'RESULTS'
        return season

    def getSeasonTabs(self) -> List[PageElement]:
        # ['NEXT MATCHES', 'RESULTS', 'STANDINGS', 'OUTRIGHTS', list of seasons]
        pes = self.browser.find_elements(leaguePage.navigation.seasons)
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
        for row in self.browser.find_elements(leaguePage.grid):
            cl = row.get_attribute('class')
            if 'deactivate' in cl:  # матч
                m = Match().parse(self.browser, border, row)
                if m.bkNum is None:
                    print('>!> invalid bk odds: {}'.format(self.browser.current_url))
                    raise ValueError
                if m.finished:
                    matches.append(m)
            elif 'nob-border' in cl:  # дата
                border.update(self.browser, row)
            elif 'dark center' in cl:  # шапка
                continue
            elif 'table-dummyrow' in cl:  # пустая строка
                continue
            elif cl == 'odd' or cl == '':  # new match without score
                continue
            else:
                print('help paksportgrab -> leagueGrid -> grab(): ', [cl])
                raise StopIteration(cl)
        return matches

    def nextPage(self):
        def isGotNext():
            if self.browser.is_on_page(leaguePage.navigation.buttons):
                return current in self.getNavigationButtons()

        current = self.browser.find_element(leaguePage.navigation.currentPage).text
        btn = self.getNavigationButtons()[leaguePage.navigation.nextButton]
        url = btn.get_attribute('href')
        self.browser.go(url, until=[self.isLoadedGrid, isGotNext], empty=self.isEmpty, reload=self.isReload)

    def isEndOfSeason(self) -> bool:
        if not self.isVisibleNavigationButtons():
            return True

        buttons = self.getNavigationButtons()
        urls = {key: pe.get_attribute('href') for key, pe in buttons.items()}
        if urls[leaguePage.navigation.nextButton] == urls[leaguePage.navigation.endButton]:
            if list(urls.values()).count(urls[leaguePage.navigation.endButton]) == 2:
                return True

    def isLoadedGrid(self) -> bool:
        return self.browser.is_on_page(leaguePage.gridElement)

    def isVisibleNavigationButtons(self) -> bool:
        return self.browser.is_on_page(leaguePage.navigation.buttons)

    def isVisibleSeasonTabs(self) -> bool:
        return self.browser.is_on_page(leaguePage.navigation.seasons)
