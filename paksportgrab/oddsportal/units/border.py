from paklib import datetimeutils
from pakselenium.browser import Browser, PageElement

from .. import utils


class Border(object):
    sport: str
    country: str
    league: str
    leagueUrl: str
    date: str
    oddsType: list

    def update(self, browser: Browser, pe: PageElement):
        raise StopIteration


class SportGridBorder(Border):

    def update(self, browser: Browser, pe: PageElement):
        # [country, league]
        pes = browser.findElementsFrom(pe, 'th > a')
        assert len(pes) == 2
        country, league = pes
        self.country = country.text
        self.league = league.text
        self.leagueUrl = league.getAttribute('href') + 'results/'

        # [cl, *odds, bkNum]
        pes = browser.findElementsFrom(pe, 'th')
        self.oddsType = [i.text for i in pes[1:-1]]


class LeagueGridBorder(Border):

    def update(self, browser: Browser, pe: PageElement):
        pes = browser.findElementsFrom(pe, 'th')
        date, *odds, bk = [i.text for i in pes]
        self.date = self.getCorrectDate(date)
        self.oddsType = odds

    @staticmethod
    def getCorrectDate(date):
        if 'Tomorrow' in date:
            today = datetimeutils.today()
            return datetimeutils.datetimeOtherDay(today, 1)
        if 'Today' in date:
            return datetimeutils.today()
        if 'Yesterday' in date:
            today = datetimeutils.today()
            return datetimeutils.datetimeOtherDay(today, -1)
        return utils.getDateFromString(date)
