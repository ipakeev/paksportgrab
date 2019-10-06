from typing import List
from pakselenium import Browser

from . import utils
from .config.selector import sportPage
from .grid import Grid
from .units.border import SportGridBorder
from .units.sport import Sport
from .units.league import League
from .units.match import Match


def catchExceptions(func):
    def wrapper(self, *args, **kwargs):
        while 1:
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                if self.isReload():
                    self.browser.refresh(until=self.isLoadedGrid)
                    continue
                print('msg: {}'.format(self.msg))
                raise e

    return wrapper


class SportGrid(Grid):
    browser: Browser

    def __init__(self, browser: Browser):
        super().__init__()
        self.browser = browser
        self.msgSelector = sportPage.msg

    def getCurrentDate(self) -> str:
        pe = self.browser.findElement(sportPage.date)
        return utils.getDateFromString(pe.text)

    def getCurrentSport(self) -> str:
        if self.browser.isOnPage(sportPage.moreSport):  # for sport in hidden tab
            pe = self.browser.findElement(sportPage.moreSport)
            if pe.text == 'More':
                pe = self.browser.findElement(sportPage.currentSport)
        else:
            pe = self.browser.findElement(sportPage.currentSport)
        return utils.getSportName(pe.text)

    def switchToEvents(self):
        if self.isSwitchedToEvents():
            return

        pe = self.browser.findElement(sportPage.eventsTab)
        self.browser.click(pe, until=(self.isLoadedGrid, self.isSwitchedToEvents))

    def switchToKickOffTime(self):
        if self.isSwitchedToKickOffTime():
            return

        pe = self.browser.findElement(sportPage.kickOffTimeTab)
        self.browser.click(pe, until=(self.isLoadedGrid, self.isSwitchedToKickOffTime))

    @catchExceptions
    def grab(self) -> List[League]:
        border = SportGridBorder()
        border.sport = self.getCurrentSport()
        border.date = self.getCurrentDate()
        sport = Sport()
        for row in self.browser.findElements(sportPage.grid):
            cl = row.getAttribute('class')
            if 'deactivate' in cl or cl == 'odd' or cl == '':  # матч
                m = Match(self.browser, border, row)
                sport.addMatch(border, m)
            elif 'dark center' in cl:  # страна, лига
                border.update(self.browser, row)
            else:
                raise StopIteration(cl)
        return sport.leagues

    def isLoadedGrid(self) -> bool:
        return self.browser.isOnPage(sportPage.gridElement)

    def isSwitchedToEvents(self) -> bool:
        return self.browser.findElement(sportPage.currentSortTab).text == 'Events'

    def isSwitchedToKickOffTime(self) -> bool:
        return self.browser.findElement(sportPage.currentSortTab).text == 'Kick off time'
