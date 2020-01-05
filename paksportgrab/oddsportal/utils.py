import datetime
from typing import Optional
from paklib import ioutils

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


def getDateSportUrl(sport: str, date: datetime.date) -> str:
    # -> 'https://www.oddsportal.com/matches/sport/date/'
    return ioutils.correctFileName([names.baseUrl, 'matches', sport, date.strftime('%Y%m%d')]) + '/'


def getDateFromString(s: str) -> datetime.date:
    day, month, year = reCompiled.date.findall(s)[0]
    return datetime.datetime.strptime(f'{day} {month} {year}', '%d %b %Y').date()


def getDateTimeFromString(s: str) -> datetime.datetime:
    day, month, year, tt = reCompiled.dateTime.findall(s)[0]
    date = datetime.datetime.strptime(f'{day} {month} {year}', '%d %b %Y').date()
    time = datetime.time.fromisoformat(tt)
    return datetime.datetime.combine(date, time)


def getOddValue(s: str) -> float:
    value = reCompiled.oddValue.findall(s)[0]
    return float(value)
