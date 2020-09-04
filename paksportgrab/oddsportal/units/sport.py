from typing import List

from .border import SportGridBorder
from .league import League
from .match import Match


class Sport(object):
    leagues: List[League]

    def __init__(self):
        self.leagues = []

    @staticmethod
    def is_equal(border: SportGridBorder, league: League):
        if border.league_url and (border.league_url == league.league_url):
            return True
        if border.sport and (border.sport == league.sport):
            if border.country and (border.country == league.country):
                if border.league == league.league:
                    return True
        return False

    def get_league(self, border: SportGridBorder) -> League:
        for league in self.leagues:
            if self.is_equal(border, league):
                return league

        league = League().parse(border)
        self.leagues.append(league)
        return league

    def add_match(self, border: SportGridBorder, m: Match):
        league = self.get_league(border)
        league.add_next_match(m)
