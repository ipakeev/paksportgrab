import datetime
from typing import List, Optional

from paklib import ioutils

from .config import names
from .config.selector import reCompiled


def getSportName(name: str) -> str:
    return names.sportName[name]


def getMatchTabName(name: str) -> Optional[str]:
    if not name:
        return
    if name in names.tabName:
        return names.tabName[name]
    raise KeyError(f'>!> Unknown tab: {name}')


def getMatchSubTabName(name: str) -> Optional[str]:
    if not name:
        return
    if name in names.subTabName:
        return names.subTabName[name]
    raise KeyError(f'>!> Unknown tab: {name}')


def getMatchId(url: str) -> str:
    # 'https://www.oddsportal.com/soccer/spain/laliga/atl-madrid-real-madrid-I9OmRkES/' -> 'I9OmRkES'
    assert names.baseUrl in url
    if '#' in url:
        url = url[:url.index('#')]
    matchId = url[url.rindex('-') + 1:]
    matchId = matchId[:matchId.index('/')]
    assert matchId
    return matchId


def getDateSportUrl(sport: str, date: datetime.date) -> str:
    # -> 'https://www.oddsportal.com/matches/sport/date/'
    return ioutils.correctFileName([names.baseUrl, 'matches', sport, date.strftime('%Y%m%d')]) + '/'


def getDateFromString(s: str) -> datetime.date:
    day, month, year = reCompiled.date.findall(s)[0]
    try:
        return datetime.datetime.strptime(f'{day} {month} {year}', '%d %b %Y').date()
    except ValueError:
        return datetime.datetime.strptime(f'{day} {month} {year}', '%d %B %Y').date()


def getDateTimeFromString(s: str) -> datetime.datetime:
    day, month, year, tt = reCompiled.dateTime.findall(s)[0]
    try:
        date = datetime.datetime.strptime(f'{day} {month} {year}', '%d %b %Y').date()
    except ValueError:
        date = datetime.datetime.strptime(f'{day} {month} {year}', '%d %B %Y').date()
    time = datetime.time.fromisoformat(tt)
    return datetime.datetime.combine(date, time)


def getOddValue(s: str) -> float:
    value = reCompiled.oddValue.findall(s)[0]
    return float(value)


class isReachedUrl:
    def __init__(self, url: str):
        self.url = url
        self.target = self.splitUrl(self.url)

    def __call__(self, driver):
        return self.isEqual(driver.current_url)

    def isEqual(self, currentUrl):
        if self.url == currentUrl:
            return True

        if '/#/page/' in self.url:
            return self.url == currentUrl
        elif self.target[-1] == 'results':
            current = self.splitUrl(currentUrl)
            if current[:4] == self.target[:4] and current[5:] == self.target[5:]:
                return True
            else:
                return False
        elif len(self.target) == 6:
            return getMatchId(self.url) == getMatchId(currentUrl)
        else:
            return self.url == currentUrl

    @staticmethod
    def splitUrl(url: str) -> List[str]:
        url = url.split('/')
        stop = [i for i in url if i.startswith('#')]
        if stop:
            url = url[:url.index(stop[0])]
        return [i for i in url if i]
