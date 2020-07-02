import datetime
from typing import List, Optional, NamedTuple

from .border import Border
from .match import Match


class SeasonDescribe(NamedTuple):
    name: str
    url: str


class League(object):
    skip: False
    sport: str
    country: str
    league: str
    leagueId: Optional[int]
    leagueUrl: str
    nextMatches: List[Match]

    def parse(self, border: Border):
        self.skip = False
        self.sport = border.sport
        self.country = border.country
        self.league = border.league
        self.leagueId = None
        self.leagueUrl = border.leagueUrl
        self.nextMatches = []

        return self

    def setToMatch(self, m):
        m.sport = self.sport
        m.country = self.country
        m.league = self.league
        m.leagueId = self.leagueId

    def addNextMatch(self, m: Match):
        m.createdAt = datetime.datetime.today()
        self.setToMatch(m)
        self.nextMatches.append(m)
