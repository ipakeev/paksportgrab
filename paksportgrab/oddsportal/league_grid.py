from typing import Tuple, List, Dict

from pakselenium import Browser, PageElement, catch

from .config import GLOBAL
from .config.selector import league_page
from .grid import Grid
from .units.border import LeagueGridBorder
from .units.match import Match


def catch_exceptions(func):
    def wrapper(self, *args, **kwargs):
        if GLOBAL.debug:
            return func(self, *args, **kwargs)

        while 1:
            try:
                return func(self, *args, **kwargs)
            except ValueError:
                self.browser.refresh(until=self.is_loaded_grid)
            except Exception as e:
                if self.is_reload():
                    self.browser.refresh(until=self.is_loaded_grid)
                    continue
                print('msg: {}'.format(self.msg))
                raise e

    return wrapper


class LeagueGrid(Grid):
    browser: Browser

    def __init__(self, browser: Browser):
        super().__init__()
        self.browser = browser

    def get_SCL(self) -> Tuple[str, str, str]:
        # ['/', sport, country, league]
        pes = self.browser.find_elements(league_page.SCL)
        _, sport, country, league = [i.text for i in pes]
        league = league.replace(self.get_current_season_name(), '').strip()
        return sport, country, league

    def get_navigation_buttons(self) -> Dict[str, PageElement]:
        pes = self.browser.find_elements(league_page.navigation.buttons)
        buttons = {i.text: i for i in pes}
        return buttons

    def get_current_season_name(self) -> str:
        # ['RESULTS', current season]
        pes = self.browser.find_elements(league_page.navigation.current_season)
        tab, season = [i.text for i in pes]
        assert tab == 'RESULTS'
        return season

    def get_season_tabs(self) -> List[PageElement]:
        # ['NEXT MATCHES', 'RESULTS', 'STANDINGS', 'OUTRIGHTS', list of seasons]
        pes = self.browser.find_elements(league_page.navigation.seasons)
        seasons = [i for i in pes if i.text not in league_page.ignore_tabs]

        # sort seasons, first current season
        current = self.get_current_season_name()
        index = [n for n, i in enumerate(seasons) if i.text == current][0]
        current = seasons.pop(index)

        return [current] + seasons

    @catch_exceptions
    def grab(self) -> List[Match]:
        border = LeagueGridBorder()
        matches = []
        for row in self.browser.find_elements(league_page.grid):
            cl = row.get_attribute('class')
            if 'deactivate' in cl:  # матч
                m = Match().parse(self.browser, border, row)
                if m.bk_num is None:
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

    def next_page(self):
        def is_got_next():
            if self.browser.is_on_page(league_page.navigation.buttons):
                return current in self.get_navigation_buttons()

        current = self.browser.find_element(league_page.navigation.current_page).text
        btn = self.get_navigation_buttons()[league_page.navigation.next_button]
        url = btn.get_attribute('href')

        @catch.timeoutException(lambda: self.browser.refresh())
        def go():
            self.browser.go(url, until=[self.is_loaded_grid, is_got_next], empty=self.is_empty, reload=self.is_reload)

        go()

    def is_end_of_season(self) -> bool:
        if not self.is_visible_navigation_buttons():
            return True

        buttons = self.get_navigation_buttons()
        urls = {key: pe.get_attribute('href') for key, pe in buttons.items()}
        if urls[league_page.navigation.next_button] == urls[league_page.navigation.end_button]:
            if list(urls.values()).count(urls[league_page.navigation.end_button]) == 2:
                return True

    def is_loaded_grid(self) -> bool:
        return self.browser.is_on_page(league_page.grid_element)

    def is_visible_navigation_buttons(self) -> bool:
        return self.browser.is_on_page(league_page.navigation.buttons)

    def is_visible_season_tabs(self) -> bool:
        return self.browser.is_on_page(league_page.navigation.seasons)
