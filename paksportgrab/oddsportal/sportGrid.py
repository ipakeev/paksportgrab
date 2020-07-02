import datetime
from typing import List

from pakselenium import Browser

from . import utils
from .config import GLOBAL
from .config.selector import sportPage
from .grid import Grid
from .units.border import SportGridBorder
from .units.league import League
from .units.match import Match
from .units.sport import Sport


def catchExceptions(func):
    def wrapper(self, *args, **kwargs):
        if GLOBAL.debug:
            return func(self, *args, **kwargs)

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

    def getCurrentDate(self) -> datetime.date:
        pe = self.browser.find_element(sportPage.date)
        return utils.getDateFromString(pe.text)

    def getCurrentSport(self) -> str:
        if self.browser.is_on_page(sportPage.moreSport):  # for sport in hidden tab
            pe = self.browser.find_element(sportPage.moreSport)
            if not pe.text or pe.text == 'More':
                pe = self.browser.find_element(sportPage.currentSport)
        else:
            pe = self.browser.find_element(sportPage.currentSport)
        return utils.getSportName(pe.text)

    def switchToEvents(self):
        if self.isSwitchedToEvents():
            return
        self.browser.click(sportPage.eventsTab, until=[self.isLoadedGrid, self.isSwitchedToEvents])

    def switchToKickOffTime(self):
        if self.isSwitchedToKickOffTime():
            return
        self.browser.click(sportPage.kickOffTimeTab, until=[self.isLoadedGrid, self.isSwitchedToKickOffTime])

    @catchExceptions
    def grab(self) -> List[League]:
        border = SportGridBorder()
        border.sport = self.getCurrentSport()
        border.date = self.getCurrentDate()
        sport = Sport()
        for row in self.browser.find_elements(sportPage.grid):
            cl = row.get_attribute('class')
            if 'deactivate' in cl or cl == 'odd' or cl == '':  # матч
                m = Match().parse(self.browser, border, row)
                sport.addMatch(border, m)
            elif cl == 'center nob-border':  # иногда выскакивает, если матчи будут скоро
                continue
            elif 'dark center' in cl:  # страна, лига
                border.update(self.browser, row)
            else:
                raise StopIteration(cl)
        return sport.leagues

    def isLoadedGrid(self) -> bool:
        return self.browser.is_on_page(sportPage.gridElement)

    def isSwitchedToEvents(self) -> bool:
        return self.browser.find_element(sportPage.currentSortTab).text == 'Events'

    def isSwitchedToKickOffTime(self) -> bool:
        return self.browser.find_element(sportPage.currentSortTab).text == 'Kick off time'
