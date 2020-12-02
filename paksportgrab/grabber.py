import datetime
import re
import time
from functools import partial
from typing import Optional, Union, List, Callable

from pakselenium import Browser, Selector
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, TimeoutException

from .oddsportal import utils
from .oddsportal.config import names, GLOBAL
from .oddsportal.league_grid import LeagueGrid
from .oddsportal.match_grid import MatchGrid
from .oddsportal.sport_grid import SportGrid
from .oddsportal.units.league import League, SeasonDescribe
from .oddsportal.units.match import Match
from .oddsportal.user import User


def catch_exceptions(func):
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
            except TimeoutException:
                # when error loading page
                self.browser.refresh()
            except AssertionError:
                # when unknown error (tab name)
                print('>!> Assertion error')
                print(func, args, kwargs)
            except WebDriverException:
                # when browser is closed
                crash += 1
                if crash == 5:
                    print('>!> new session')
                    self.new_browser_session()
                    crash = 0
            except Exception as e:
                print(func, args, kwargs)
                raise e
            time.sleep(1)

    return wrapper


class Grabber:
    browser: Browser
    user: User
    sport_grid: SportGrid
    league_grid: LeagueGrid
    match_grid: MatchGrid

    def __init__(self, browser: Browser, cookie_path: str = None):
        self.browser = browser
        self.browser.go = partial(self.browser.go, is_reached_url=utils.is_reached_url)
        self.user = User(self.browser)
        self.sport_grid = SportGrid(self.browser)
        self.league_grid = LeagueGrid(self.browser)
        self.match_grid = MatchGrid(self.browser)

        if cookie_path is not None:
            names.cookie_path = cookie_path

    def new_browser_session(self):
        self.browser.new_session()
        self.user.login()

    def login(self, username: str, password: str):
        self.user.set_login_data(username, password)
        self.user.login()

    def go(self, url: str,
           until: Union[Callable, List[Callable]] = None,
           until_lost: Union[Selector, List[Selector]] = None,
           empty: Callable = None,
           reload: Callable = None):
        while 1:
            self.browser.go(url, until=until, until_lost=until_lost, empty=empty, reload=reload)
            if self.user.is_logged_in():
                break
            else:
                self.user.login()

    @catch_exceptions
    def get_leagues(self, sport: str, date: datetime.date) -> Optional[List[League]]:
        url = utils.get_date_sport_url(sport, date)

        self.go(url, until=self.sport_grid.is_loaded_grid,
                empty=self.sport_grid.is_empty, reload=self.sport_grid.is_reload)

        if self.sport_grid.is_empty():
            return None

        self.sport_grid.switch_to_events()
        return self.sport_grid.grab()

    @catch_exceptions
    def get_seasons(self, league_url: str) -> List[SeasonDescribe]:
        self.go(league_url, until=self.league_grid.is_loaded_grid,
                empty=self.league_grid.is_empty, reload=self.league_grid.is_reload)

        if self.league_grid.is_visible_season_tabs():
            seasons = self.league_grid.get_season_tabs()
            return [SeasonDescribe(name=i.text, url=i.get_attribute('href')) for i in seasons]
        else:
            return []

    @catch_exceptions
    def get_matches(self, league_url: str, till_match_id: str = None,
                    seasons_depth: int = 5, season_min='2014') -> List[Match]:
        def is_reached_season():
            if self.league_grid.is_visible_season_tabs():
                return self.league_grid.get_current_season_name() == season_name

        self.go(league_url, until=self.league_grid.is_loaded_grid,
                empty=self.league_grid.is_empty, reload=self.league_grid.is_reload)

        matches = []

        if self.league_grid.is_empty():
            return matches

        season_elements = self.league_grid.get_season_tabs()
        seasons_urls = {i.text: i.get_attribute('href') for i in season_elements}
        season_names = [i.text for i in season_elements]  # new list because needs course of seasons
        start = [i.get_attribute('href') for i in season_elements].index(league_url)
        assert start < seasons_depth
        season_names = season_names[start:seasons_depth]

        for season_name in season_names:
            if re.findall(r'(\d{4})', season_name)[0] < season_min:
                continue
            url = seasons_urls[season_name]
            if not is_reached_season():
                self.go(url, until=[self.league_grid.is_loaded_grid, is_reached_season],
                        empty=self.league_grid.is_empty, reload=self.league_grid.is_reload)

            if not self.league_grid.is_empty():
                while 1:
                    new = self.league_grid.grab()
                    for m in new:
                        m.season = season_name
                    matches.extend(new)

                    if till_match_id:
                        if till_match_id in [i.id for i in new]:
                            return matches

                    if self.league_grid.is_end_of_season():
                        break
                    self.league_grid.next_page()

            season_elements = self.league_grid.get_season_tabs()
            seasons_urls = {i.text: i.get_attribute('href') for i in season_elements}

        return matches

    @catch_exceptions
    def fill_match(self, match: Match, fill_finished=False):
        if match.filled_score and match.filled_odds:
            return
        odds_tabs = names.sport_tabs[match.sport]

        def get_tabs_name_list():
            current = self.match_grid.get_current_tab_name()
            tabs_name_list = list(odds_tabs.keys())
            if current in tabs_name_list:
                return [current] + [i for i in tabs_name_list if (i != current and i in tabs)]
            else:
                return [i for i in tabs_name_list if i in tabs]

        def get_sub_tabs_name_list():
            current = self.match_grid.get_current_sub_tab_name()
            sub_tabs_name_list = odds_tabs[tab_name]
            if current in sub_tabs_name_list:
                return [current] + [i for i in sub_tabs_name_list if (i != current and i in sub_tabs)]
            else:
                return [i for i in sub_tabs_name_list if i in sub_tabs]

        def is_reached_tab():
            return self.match_grid.get_current_tab_name() == tab_name

        def is_reached_sub_tab():
            return self.match_grid.get_current_sub_tab_name() == sub_tab_name

        self.go(match.url, until=self.match_grid.is_loaded_grid,
                empty=self.match_grid.is_empty, reload=self.match_grid.is_reload)

        match.updated_at = datetime.datetime.today()
        match.date_time = self.match_grid.get_date_time()
        match.score_string = self.match_grid.get_result()
        match.score = None

        if match.score_string:
            match.set_finished()
            match.filled_score = True

        if fill_finished and not match.finished:
            return

        if match.filled_odds:
            return

        for tab_name in odds_tabs.keys():
            match.odds[tab_name] = {sub_tab_name: None for sub_tab_name in odds_tabs[tab_name]}

        if self.match_grid.is_empty():
            match.filled_odds = True
            return

        tabs = self.match_grid.get_tabs()
        for tab_name in get_tabs_name_list():
            if not is_reached_tab():
                self.browser.click(tabs[tab_name],
                                   until=[self.match_grid.is_loaded_grid, is_reached_tab],
                                   reload=self.match_grid.is_reload)

            sub_tabs = self.match_grid.get_sub_tabs()
            for sub_tab_name in get_sub_tabs_name_list():
                if not is_reached_sub_tab():
                    self.browser.click(sub_tabs[sub_tab_name],
                                       until=[self.match_grid.is_loaded_grid, is_reached_tab, is_reached_sub_tab],
                                       reload=self.match_grid.is_reload)

                match.odds[tab_name][sub_tab_name] = self.match_grid.grab(tab_name)

        match.filled_odds = True

    def test_match(self, sport: str, url: str):
        odds_tabs = names.sport_tabs[sport]

        def get_tabs_name_list():
            current = self.match_grid.get_current_tab_name()
            tabs_name_list = list(odds_tabs.keys())
            if current in tabs_name_list:
                return [current] + [i for i in tabs_name_list if (i != current and i in tabs)]
            else:
                return [i for i in tabs_name_list if i in tabs]

        def get_sub_tabs_name_list():
            current = self.match_grid.get_current_sub_tab_name()
            sub_tabs_name_list = odds_tabs[tab_name]
            if current in sub_tabs_name_list:
                return [current] + [i for i in sub_tabs_name_list if (i != current and i in subTabs)]
            else:
                return [i for i in sub_tabs_name_list if i in subTabs]

        def is_reached_tab():
            return self.match_grid.get_current_tab_name() == tab_name

        def is_reached_sub_tab():
            return self.match_grid.get_current_sub_tab_name() == sub_tab_name

        print(f'isReachedUrl: {utils.is_reached_url(url)(self.browser.driver)}')
        print(f'target: {url}, current: {self.browser.current_url}')

        print(f'isLoadedGrid: {self.match_grid.is_loaded_grid()}')
        print(f'isEmpty: {self.match_grid.is_empty()}')
        print(f'isReload: {self.match_grid.is_reload()}')

        odds = {}
        for tab_name in odds_tabs.keys():
            odds[tab_name] = {sub_tab_name: None for sub_tab_name in odds_tabs[tab_name]}

        tabs = self.match_grid.get_tabs()
        print(f'tabs: {tabs.keys()}')
        for tab_name in get_tabs_name_list():
            print(f'> tab: {tab_name}')
            if not is_reached_tab():
                print(f'click on {tab_name}')
                self.browser.click(tabs[tab_name],
                                   until=[self.match_grid.is_loaded_grid, is_reached_tab],
                                   reload=self.match_grid.is_reload)
                print(f'res: [{self.match_grid.is_loaded_grid()}, {is_reached_tab()}], [{self.match_grid.is_reload()}')

            subTabs = self.match_grid.get_sub_tabs()
            print(f'subTabs: {subTabs}')
            for sub_tab_name in get_sub_tabs_name_list():
                print(f'> subTab: {sub_tab_name}')
                if not is_reached_sub_tab():
                    print(f'click on {sub_tab_name}')
                    self.browser.click(subTabs[sub_tab_name],
                                       until=[self.match_grid.is_loaded_grid, is_reached_sub_tab],
                                       reload=self.match_grid.is_reload)
                    print(f'res: [{self.match_grid.is_loaded_grid()}, '
                          f'{is_reached_sub_tab()}], [{self.match_grid.is_reload()}')

                print(self.match_grid.grab(tab_name))
