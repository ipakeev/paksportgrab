import datetime

from pakselenium import Browser, PageElement, Selector, By

from .. import utils


class Border(object):
    sport: str
    country: str
    league: str
    leagueUrl: str
    date: datetime.date
    oddsType: list

    def update(self, browser: Browser, pe: PageElement):
        raise StopIteration


class SportGridBorder(Border):

    def update(self, browser: Browser, pe: PageElement):
        # [country, league]
        pes = browser.find_elements_from(pe, Selector(By.CSS_SELECTOR, 'th > a'))
        assert len(pes) == 2
        country, league = pes
        self.country = country.text
        self.league = league.text
        self.leagueUrl = league.get_attribute('href') + 'results/'

        # [cl, *odds, bkNum]
        pes = browser.find_elements_from(pe, Selector(By.CSS_SELECTOR, 'th'))
        self.oddsType = [i.text for i in pes[1:-1]]


class LeagueGridBorder(Border):

    def update(self, browser: Browser, pe: PageElement):
        pes = browser.find_elements_from(pe, Selector(By.CSS_SELECTOR, 'th'))
        date, *odds, bk = [i.text for i in pes]
        self.date = self.getCorrectDate(date)
        self.oddsType = odds

    @staticmethod
    def getCorrectDate(date: str) -> datetime.date:
        # date = '19 Sep 2019'
        if 'Tomorrow' in date:
            today = datetime.date.today()
            return today + datetime.timedelta(days=1)
        if 'Today' in date:
            return datetime.date.today()
        if 'Yesterday' in date:
            today = datetime.date.today()
            return today - datetime.timedelta(days=1)
        return utils.getDateFromString(date)
