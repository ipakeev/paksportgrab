import datetime
from typing import List, Optional

from paklib import io

from .config import names
from .config.selector import re_compiled


def get_sport_name(name: str) -> str:
    return names.sport_name[name]


def get_match_tab_name(name: str) -> Optional[str]:
    if not name:
        return
    if name in names.tab_name:
        return names.tab_name[name]
    print(f'>!> Unknown tab: {name}')
    return


def get_match_sub_tab_name(name: str) -> Optional[str]:
    if not name:
        return
    if name in names.sub_tab_name:
        return names.sub_tab_name[name]
    print(f'>!> Unknown tab: {name}')
    return


def get_match_id(url: str) -> str:
    # 'https://www.oddsportal.com/soccer/spain/laliga/atl-madrid-real-madrid-I9OmRkES/' -> 'I9OmRkES'
    assert names.base_url in url
    if '#' in url:
        url = url[:url.index('#')]
    match_id = url[url.rindex('-') + 1:]
    match_id = match_id[:match_id.index('/')]
    assert match_id
    return match_id


def get_date_sport_url(sport: str, date: datetime.date) -> str:
    # -> 'https://www.oddsportal.com/matches/sport/date/'
    return io.correct_file_name([names.base_url, 'matches', sport, date.strftime('%Y%m%d')]) + '/'


def get_date_from_string(s: str) -> datetime.date:
    day, month, year = re_compiled.date.findall(s)[0]
    try:
        return datetime.datetime.strptime(f'{day} {month} {year}', '%d %b %Y').date()
    except ValueError:
        return datetime.datetime.strptime(f'{day} {month} {year}', '%d %B %Y').date()


def get_date_time_from_string(s: str) -> datetime.datetime:
    day, month, year, tt = re_compiled.date_time.findall(s)[0]
    try:
        date = datetime.datetime.strptime(f'{day} {month} {year}', '%d %b %Y').date()
    except ValueError:
        date = datetime.datetime.strptime(f'{day} {month} {year}', '%d %B %Y').date()
    time = datetime.time.fromisoformat(tt)
    return datetime.datetime.combine(date, time)


def get_odd_value(s: str) -> float:
    value = re_compiled.odd_value.findall(s)[0]
    return float(value)


class is_reached_url:
    def __init__(self, url: str):
        self.url = url
        self.target = self.split_url(self.url)

    def __call__(self, driver):
        return self.is_equal(driver.current_url)

    def is_equal(self, current_url):
        if self.url == current_url:
            return True

        if '/#/page/' in self.url:
            return self.url == current_url
        elif self.target[-1] == 'results':
            current = self.split_url(current_url)
            if current[:4] == self.target[:4] and current[5:] == self.target[5:]:
                return True
            else:
                return False
        elif len(self.target) == 6:
            return get_match_id(self.url) == get_match_id(current_url)
        else:
            return self.url == current_url

    @staticmethod
    def split_url(url: str) -> List[str]:
        url = url.split('/')
        stop = [i for i in url if i.startswith('#')]
        if stop:
            url = url[:url.index(stop[0])]
        return [i for i in url if i]
