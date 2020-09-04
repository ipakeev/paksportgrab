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
    league_id: Optional[int]
    league_url: str
    next_matches: List[Match]

    def parse(self, border: Border):
        self.skip = False
        self.sport = border.sport
        self.country = border.country
        self.league = border.league
        self.league_id = None
        self.league_url = border.league_url
        self.next_matches = []

        return self

    def set_to_match(self, m):
        m.sport = self.sport
        m.country = self.country
        m.league = self.league
        m.league_id = self.league_id

    def add_next_match(self, m: Match):
        m.created_at = datetime.datetime.today()
        self.set_to_match(m)
        self.next_matches.append(m)
