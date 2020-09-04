import datetime
from typing import List

from pakselenium import Browser

from . import utils
from .config import GLOBAL
from .config.selector import sport_page
from .grid import Grid
from .units.border import SportGridBorder
from .units.league import League
from .units.match import Match
from .units.sport import Sport


def catch_exceptions(func):
    def wrapper(self, *args, **kwargs):
        if GLOBAL.debug:
            return func(self, *args, **kwargs)

        while 1:
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                if self.is_reload():
                    self.browser.refresh(until=self.is_loaded_grid)
                    continue
                print('msg: {}'.format(self.msg))
                raise e

    return wrapper


class SportGrid(Grid):
    browser: Browser

    def __init__(self, browser: Browser):
        super().__init__()
        self.browser = browser

    def get_current_date(self) -> datetime.date:
        pe = self.browser.find_element(sport_page.date)
        return utils.get_date_from_string(pe.text)

    def get_current_sport(self) -> str:
        if self.browser.is_on_page(sport_page.more_sport):  # for sport in hidden tab
            pe = self.browser.find_element(sport_page.more_sport)
            if not pe.text or pe.text == 'More':
                pe = self.browser.find_element(sport_page.current_sport)
        else:
            pe = self.browser.find_element(sport_page.current_sport)
        return utils.get_sport_name(pe.text)

    def switch_to_events(self):
        if self.is_switched_to_events():
            return
        self.browser.click(sport_page.events_tab, until=[self.is_loaded_grid, self.is_switched_to_events])

    def switch_to_kick_off_time(self):
        if self.is_switched_to_kick_off_time():
            return
        self.browser.click(sport_page.kick_off_time_tab, until=[self.is_loaded_grid,
                                                                self.is_switched_to_kick_off_time])

    @catch_exceptions
    def grab(self) -> List[League]:
        border = SportGridBorder()
        border.sport = self.get_current_sport()
        border.date = self.get_current_date()
        sport = Sport()
        for row in self.browser.find_elements(sport_page.grid):
            cl = row.get_attribute('class')
            if 'deactivate' in cl or cl == 'odd' or cl == '':  # матч
                m = Match().parse(self.browser, border, row)
                sport.add_match(border, m)
            elif cl == 'center nob-border':  # иногда выскакивает, если матчи будут скоро
                continue
            elif 'dark center' in cl:  # страна, лига
                border.update(self.browser, row)
            else:
                raise StopIteration(cl)
        return sport.leagues

    def is_loaded_grid(self) -> bool:
        return self.browser.is_on_page(sport_page.grid_element)

    def is_switched_to_events(self) -> bool:
        return self.browser.find_element(sport_page.current_sort_tab).text == 'Events'

    def is_switched_to_kick_off_time(self) -> bool:
        return self.browser.find_element(sport_page.current_sort_tab).text == 'Kick off time'
