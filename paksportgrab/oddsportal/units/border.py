import datetime

from pakselenium import Browser, PageElement, Selector, By

from paksportgrab.oddsportal import utils


class Border(object):
    sport: str
    country: str
    league: str
    league_url: str
    date: datetime.date
    odds_type: list

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
        self.league_url = league.get_attribute('href') + 'results/'

        # [cl, *odds, bkNum]
        pes = browser.find_elements_from(pe, Selector(By.CSS_SELECTOR, 'th'))
        self.odds_type = [i.text for i in pes[1:-1]]


class LeagueGridBorder(Border):

    def update(self, browser: Browser, pe: PageElement):
        pes = browser.find_elements_from(pe, Selector(By.CSS_SELECTOR, 'th'))
        date, *odds, bk = [i.text for i in pes]
        self.date = self.get_correct_date(date)
        self.odds_type = odds

    @staticmethod
    def get_correct_date(date: str) -> datetime.date:
        # date = '19 Sep 2019'
        if 'Tomorrow' in date:
            today = datetime.date.today()
            return today + datetime.timedelta(days=1)
        if 'Today' in date:
            return datetime.date.today()
        if 'Yesterday' in date:
            today = datetime.date.today()
            return today - datetime.timedelta(days=1)
        return utils.get_date_from_string(date)
