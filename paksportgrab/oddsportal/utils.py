from typing import Optional
from paklib import ioutils, datetimeutils

from .config.selector import reCompiled
from .config import names


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
    raise KeyError(f'>!> Unknown subTab: {name}')


def getMatchId(url: str) -> str:
    # 'https://www.oddsportal.com/soccer/spain/laliga/atl-madrid-real-madrid-I9OmRkES/' -> 'I9OmRkES'
    assert names.baseUrl in url
    matchId = url[url.rindex('-') + 1:]
    if matchId[-1] == '/':
        matchId = matchId[:-1]
    assert matchId
    return matchId


def getDateFromString(string) -> str:
    # '19 Sep 2019' -> '20190919'
    date = reCompiled.date.findall(string)[0]
    day = date[0]
    month = datetimeutils.getMonthCode(date[1])
    year = date[2]
    return year + month + day


def getDateSportUrl(sport, date) -> str:
    # -> 'https://www.oddsportal.com/matches/sport/date/'
    return ioutils.correctFileName([names.baseUrl, 'matches', sport, date]) + '/'
