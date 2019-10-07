from typing import List, Optional

from .border import Border
from .match import Match


class League(object):
    sport: str
    country: str
    league: str
    leagueId: Optional[int]
    leagueUrl: str
    nextMatches: List[Match]
    seasons: List[str]

    def __init__(self, border: Border):
        self.sport = border.sport
        self.country = border.country
        self.league = border.league
        self.leagueId = None
        self.leagueUrl = border.leagueUrl
        self.nextMatches = []

    def setToMatch(self, m):
        m.sport = self.sport
        m.country = self.country
        m.league = self.league
        m.leagueId = self.leagueId

    def addNextMatch(self, m: Match):
        self.setToMatch(m)
        self.nextMatches.append(m)
