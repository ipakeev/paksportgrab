from typing import Optional, Tuple, List, Dict
from paklib import datetimeutils
from pakselenium import Browser
from pakselenium.browser import PageElement

from . import utils
from .config import names
from .config.selector import matchPage
from .config.selector import reCompiled
from .grid import Grid


def catchExceptions(func):
    def wrapper(self, *args, **kwargs):
        while 1:
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                if self.isReload():
                    self.browser.refresh(until=self.isLoadedGrid)
                    continue
                print('msg: {}'.format(self.msg))
                raise e

    return wrapper


class MatchGrid(Grid):
    browser: Browser

    def __init__(self, browser: Browser):
        super().__init__()
        self.browser = browser

    def getSCL(self) -> Tuple[str, str, str]:
        # ['/', sport, country, league]
        pes = self.browser.findElements(matchPage.SCL)
        _, sport, country, league = [i.text for i in pes]
        return sport, country, league

    def getTeams(self) -> List[str]:
        pe = self.browser.findElement(matchPage.teams)
        return pe.text.split(' - ')

    def getDateTime(self) -> Tuple[str, str]:
        pe = self.browser.findElement(matchPage.date)
        day, month, year, tt = reCompiled.dateTime.findall(pe.text)[0]
        month = datetimeutils.getMonthCode(month)
        return year + month + day, tt

    def getResult(self) -> Optional[str]:
        if not self.browser.isOnPage(matchPage.result):
            return None
        pe = self.browser.findElement(matchPage.result)
        if 'Final result' in pe.text:
            return pe.text.replace('Final result', '').strip()
        return None

    def getCurrentTabName(self) -> str:
        if self.browser.isOnPage(matchPage.moreTab):
            pe = self.browser.findElement(matchPage.moreTab)
            if not pe.text or pe.text == 'More bets':
                pe = self.browser.findElement(matchPage.currentTab)
        else:
            pe = self.browser.findElement(matchPage.currentTab)
        name = utils.getMatchTabName(pe.text)
        assert name
        return name

    def getCurrentSubTabName(self) -> str:
        pes = self.browser.findElements(matchPage.currentSubTab)
        pes = [i for i in pes if i.text]
        assert len(pes) == 1
        name = utils.getMatchSubTabName(pes[0].text)
        assert name
        return name

    def getTabs(self) -> Dict[str, PageElement]:
        if not self.isVisibleTabs():
            return {}

        # ['', '1X2', '', 'AH', 'Over/Under', 'DNB', 'EH', 'DC', '', 'CS', '', '', '', 'More bets']
        pes = self.browser.findElements(matchPage.tabs)
        tabs = {}
        for pe in pes:
            name = utils.getMatchTabName(pe.text)
            if name:
                tabs[name] = pe
        return tabs

    def getSubTabs(self) -> Dict[str, PageElement]:
        if not self.isVisibleSubTabs():
            return {}

        # ['Full Time', '1st Half', '2nd Half']
        pes = self.browser.findElements(matchPage.subTabs)
        subTabs = {}
        for pe in pes:
            name = utils.getMatchSubTabName(pe.text)
            if name:
                subTabs[name] = pe
        return subTabs

    def grab(self, tabName):
        _type = names.tableOrValueGrid[tabName]
        if _type == names.matchTableGrid:
            return self.grabTableGrid()
        elif _type == names.matchValueGrid:
            return self.grabValueGrid()
        else:
            raise ValueError(f'Unknown tab name: {tabName}')

    @catchExceptions
    def grabValueGrid(self) -> dict:
        # ['Handicap', 'Payout', 'Under', 'Over']
        pes = self.browser.findElements(matchPage.valueGridBorder)
        handicap, payout, *oddsKeys = [i.text for i in pes if i.text]
        assert handicap == 'Handicap'
        assert payout == 'Payout'
        assert len(oddsKeys) == 2
        oddsKeys = [i.lower() for i in oddsKeys]

        oddsDict = {}
        for row in self.browser.findElements(matchPage.valueGrid):
            # ['91.5%', '5.37', '1.10', '(3)', 'Compare odds']
            pes = self.browser.findElementsFrom(row, 'span')
            line = [i.text for i in pes]
            if len(set(line)) < 3:
                continue
            _, *odds, bkNum, _ = line
            if '' in odds:  # in cases when for example ['8.5', '']
                continue

            bkNum = int(bkNum[1:-1])
            if bkNum < 1:
                continue

            odds = [float(i) for i in odds]
            assert len(oddsKeys) == len(odds) == 2

            odds = {key: odd for key, odd in zip(oddsKeys, odds)}
            odds['bkNum'] = bkNum

            value = self.browser.findElementFrom(row, 'strong')
            value = reCompiled.oddValue.findall(value.text)[0]
            value = float(value)
            oddsDict[value] = odds

        return oddsDict

    @catchExceptions
    def grabTableGrid(self) -> Optional[dict]:
        # ['Bookmakers', '1', 'X', '2', 'Payout']
        # ['Bookmakers', '1', '2', 'Payout']
        pes = self.browser.findElements(matchPage.tableGridBorder)
        texts = [i.text for i in pes if i.text]
        oddsKeys = texts[:texts.index('Payout')]
        assert 2 <= len(oddsKeys) <= 3

        pes = self.browser.findElements(matchPage.tableGridElement)
        odds = [i.text for i in pes]
        odds = [float(i) if (i and i != '-') else 1.0 for i in odds]
        assert len(oddsKeys) == len(odds)
        if set(odds) == {1.0}:  # if [1.0, 1.0]
            return None

        bkNum = len(self.browser.findElements(matchPage.tableGridBkNum))

        oddsDict = {key: odd for key, odd in zip(oddsKeys, odds)}
        oddsDict['bkNum'] = bkNum
        return oddsDict

    def isLoadedGrid(self) -> bool:
        return self.browser.isOnPage(matchPage.valueGridElement) or self.browser.isOnPage(matchPage.tableGridElement)

    def isVisibleTabs(self) -> bool:
        return self.browser.isOnPage(matchPage.tabs)

    def isVisibleSubTabs(self) -> bool:
        return self.browser.isOnPage(matchPage.subTabs)
