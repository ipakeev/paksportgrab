import datetime
from typing import Optional, Tuple, List, Dict

from pakselenium import Browser, PageElement, Selector, By

from . import utils
from .config import names, GLOBAL
from .config.selector import match_page
from .grid import Grid


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


class MatchGrid(Grid):
    browser: Browser

    def __init__(self, browser: Browser):
        super().__init__()
        self.browser = browser

    def is_finished(self) -> bool:
        if not self.browser.is_on_page(match_page.result):
            return False
        pe = self.browser.find_element(match_page.result)
        if 'Final result' in pe.text:
            return True
        return False

    def get_SCL(self) -> Tuple[str, str, str]:
        # ['/', sport, country, league]
        pes = self.browser.find_elements(match_page.SCL)
        _, sport, country, league = [i.text for i in pes]
        return sport, country, league

    def get_teams(self) -> List[str]:
        pe = self.browser.find_element(match_page.teams)
        teams = pe.text.split(' - ')
        assert all([i for i in teams])
        return teams

    def get_date_time(self) -> datetime.datetime:
        pe = self.browser.find_element(match_page.date)
        return utils.get_date_time_from_string(pe.text)

    def get_result(self) -> Optional[str]:
        if not self.browser.is_on_page(match_page.result):
            return None
        pe = self.browser.find_element(match_page.result)
        if 'Final result' in pe.text:
            return pe.text.replace('Final result', '').strip()
        if pe.text == 'Canceled':
            return 'Canceled'
        return None

    def get_current_tab_name(self) -> str:
        if self.browser.is_on_page(match_page.more_tab):
            pe = self.browser.find_element(match_page.more_tab)
            if not pe.text or pe.text == 'More bets':
                pe = self.browser.find_element(match_page.current_tab)
        else:
            pe = self.browser.find_element(match_page.current_tab)
        name = utils.get_match_tab_name(pe.text)
        assert name
        return name

    def get_current_sub_tab_name(self) -> str:
        pes = self.browser.find_elements(match_page.current_sub_tab)
        pes = [i for i in pes if i.text]
        assert len(pes) == 1
        name = utils.get_match_sub_tab_name(pes[0].text)
        assert name
        return name

    def get_tabs(self) -> Dict[str, PageElement]:
        if not self.is_visible_tabs():
            return {}

        # ['', '1X2', '', 'AH', 'Over/Under', 'DNB', 'EH', 'DC', '', 'CS', '', '', '', 'More bets']
        pes = self.browser.find_elements(match_page.tabs)
        tabs = {}
        for pe in pes:
            name = utils.get_match_tab_name(pe.text)
            if name:
                tabs[name] = pe
        return tabs

    def get_sub_tabs(self) -> Dict[str, PageElement]:
        if not self.is_visible_sub_tabs():
            return {}

        # ['Full Time', '1st Half', '2nd Half']
        pes = self.browser.find_elements(match_page.sub_tabs)
        sub_tabs = {}
        for pe in pes:
            name = utils.get_match_sub_tab_name(pe.text)
            if name:
                sub_tabs[name] = pe
        return sub_tabs

    def grab(self, tab_name):
        _type = names.tableOrValueGrid[tab_name]
        if _type == names.match_table_grid:
            return self.grab_table_grid()
        elif _type == names.match_value_grid:
            return self.grab_value_grid()
        else:
            raise ValueError(f'Unknown tab name: {tab_name}')

    @catch_exceptions
    def grab_value_grid(self) -> dict:
        # ['Handicap', 'Payout', 'Under', 'Over']
        # ['Handicap', 'Payout', '2', '1']
        pes = self.browser.find_elements(match_page.value_grid_border)
        texts = [i.text for i in pes if i.text]
        if not texts:
            return {}

        handicap, payout, *odds_keys = texts
        assert handicap == 'Handicap'
        assert payout == 'Payout'
        assert len(odds_keys) == 2
        odds_keys = [i.lower() for i in odds_keys]

        odds_dict = {}
        for row in self.browser.find_elements(match_page.value_grid):
            # ['91.5%', '5.37', '1.10', '(3)', 'Compare odds']
            pes = self.browser.find_elements_from(row, Selector(By.CSS_SELECTOR, 'span'))
            line = [i.text for i in pes]
            if len(set(line)) < 3:
                continue
            _, *odds, bk_num, _ = line
            if '' in odds:  # in cases when for example ['8.5', '']
                continue

            bk_num = int(bk_num[1:-1])
            if bk_num < 1:
                continue

            odds = [float(i) for i in odds]
            assert len(odds_keys) == len(odds) == 2

            odds = {key: odd for key, odd in zip(odds_keys, odds)}
            odds['bk_num'] = bk_num

            value = self.browser.find_element_from(row, Selector(By.CSS_SELECTOR, 'strong'))
            value = utils.get_odd_value(value.text)
            odds_dict[value] = odds

        return odds_dict

    @catch_exceptions
    def grab_table_grid(self) -> Optional[dict]:
        # ['Bookmakers', '1', 'X', '2', 'Payout']
        # ['Bookmakers', '1', '2', 'Payout']
        pes = self.browser.find_elements(match_page.table_grid_border)
        texts = [i.text for i in pes if i.text]
        if not texts:
            return {}

        odds_keys = texts[:texts.index('Payout')]
        assert 2 <= len(odds_keys) <= 3

        pes = self.browser.find_elements(match_page.table_grid_element)
        odds = [i.text for i in pes]
        odds = [float(i) if (i and i != '-') else 1.0 for i in odds]
        assert len(odds_keys) == len(odds)
        if set(odds) == {1.0}:  # if [1.0, 1.0]
            return None

        bk_num = len(self.browser.find_elements(match_page.table_grid_bk_num))

        odds_dict = {key: odd for key, odd in zip(odds_keys, odds)}
        odds_dict['bk_num'] = bk_num
        return odds_dict

    def is_loaded_grid(self) -> bool:
        return self.browser.is_on_page(match_page.value_grid_element) \
               or self.browser.is_on_page(match_page.table_grid_element)

    def is_visible_tabs(self) -> bool:
        return self.browser.is_on_page(match_page.tabs)

    def is_visible_sub_tabs(self) -> bool:
        return self.browser.is_on_page(match_page.sub_tabs)
