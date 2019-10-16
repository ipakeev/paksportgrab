from typing import List

from .border import SportGridBorder
from .league import League
from .match import Match


class Sport(object):
    leagues: List[League]

    def __init__(self):
        self.leagues = []

    @staticmethod
    def isEqual(border: SportGridBorder, league: League):
        if border.leagueUrl and (border.leagueUrl == league.leagueUrl):
            return True
        if border.sport and (border.sport == league.sport):
            if border.country and (border.country == league.country):
                if border.league == league.league:
                    return True
        return False

    def getLeague(self, border: SportGridBorder) -> League:
        for league in self.leagues:
            if self.isEqual(border, league):
                return league

        league = League().parse(border)
        self.leagues.append(league)
        return league

    def addMatch(self, border: SportGridBorder, m: Match):
        league = self.getLeague(border)
        league.addNextMatch(m)
