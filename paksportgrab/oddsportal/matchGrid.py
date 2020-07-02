import datetime
from typing import Optional, Tuple, List, Dict

from pakselenium import Browser, PageElement, Selector, By

from . import utils
from .config import names, GLOBAL
from .config.selector import matchPage
from .grid import Grid


def catchExceptions(func):
    def wrapper(self, *args, **kwargs):
        if GLOBAL.debug:
            return func(self, *args, **kwargs)

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

    def isFinished(self) -> bool:
        if not self.browser.is_on_page(matchPage.result):
            return False
        pe = self.browser.find_element(matchPage.result)
        if 'Final result' in pe.text:
            return True
        return False

    def getSCL(self) -> Tuple[str, str, str]:
        # ['/', sport, country, league]
        pes = self.browser.find_elements(matchPage.SCL)
        _, sport, country, league = [i.text for i in pes]
        return sport, country, league

    def getTeams(self) -> List[str]:
        pe = self.browser.find_element(matchPage.teams)
        teams = pe.text.split(' - ')
        assert all([i for i in teams])
        return teams

    def getDateTime(self) -> datetime.datetime:
        pe = self.browser.find_element(matchPage.date)
        return utils.getDateTimeFromString(pe.text)

    def getResult(self) -> Optional[str]:
        if not self.browser.is_on_page(matchPage.result):
            return None
        pe = self.browser.find_element(matchPage.result)
        if 'Final result' in pe.text:
            return pe.text.replace('Final result', '').strip()
        return None

    def getCurrentTabName(self) -> str:
        if self.browser.is_on_page(matchPage.moreTab):
            pe = self.browser.find_element(matchPage.moreTab)
            if not pe.text or pe.text == 'More bets':
                pe = self.browser.find_element(matchPage.currentTab)
        else:
            pe = self.browser.find_element(matchPage.currentTab)
        name = utils.getMatchTabName(pe.text)
        assert name
        return name

    def getCurrentSubTabName(self) -> str:
        pes = self.browser.find_elements(matchPage.currentSubTab)
        pes = [i for i in pes if i.text]
        assert len(pes) == 1
        name = utils.getMatchSubTabName(pes[0].text)
        assert name
        return name

    def getTabs(self) -> Dict[str, PageElement]:
        if not self.isVisibleTabs():
            return {}

        # ['', '1X2', '', 'AH', 'Over/Under', 'DNB', 'EH', 'DC', '', 'CS', '', '', '', 'More bets']
        pes = self.browser.find_elements(matchPage.tabs)
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
        pes = self.browser.find_elements(matchPage.subTabs)
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
        # ['Handicap', 'Payout', '2', '1']
        pes = self.browser.find_elements(matchPage.valueGridBorder)
        texts = [i.text for i in pes if i.text]
        if not texts:
            return {}

        handicap, payout, *oddsKeys = texts
        assert handicap == 'Handicap'
        assert payout == 'Payout'
        assert len(oddsKeys) == 2
        oddsKeys = [i.lower() for i in oddsKeys]

        oddsDict = {}
        for row in self.browser.find_elements(matchPage.valueGrid):
            # ['91.5%', '5.37', '1.10', '(3)', 'Compare odds']
            pes = self.browser.find_elements_from(row, Selector(By.CSS_SELECTOR, 'span'))
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

            value = self.browser.find_element_from(row, Selector(By.CSS_SELECTOR, 'strong'))
            value = utils.getOddValue(value.text)
            oddsDict[value] = odds

        return oddsDict

    @catchExceptions
    def grabTableGrid(self) -> Optional[dict]:
        # ['Bookmakers', '1', 'X', '2', 'Payout']
        # ['Bookmakers', '1', '2', 'Payout']
        pes = self.browser.find_elements(matchPage.tableGridBorder)
        texts = [i.text for i in pes if i.text]
        if not texts:
            return {}

        oddsKeys = texts[:texts.index('Payout')]
        assert 2 <= len(oddsKeys) <= 3

        pes = self.browser.find_elements(matchPage.tableGridElement)
        odds = [i.text for i in pes]
        odds = [float(i) if (i and i != '-') else 1.0 for i in odds]
        assert len(oddsKeys) == len(odds)
        if set(odds) == {1.0}:  # if [1.0, 1.0]
            return None

        bkNum = len(self.browser.find_elements(matchPage.tableGridBkNum))

        oddsDict = {key: odd for key, odd in zip(oddsKeys, odds)}
        oddsDict['bkNum'] = bkNum
        return oddsDict

    def isLoadedGrid(self) -> bool:
        return self.browser.is_on_page(matchPage.valueGridElement) \
               or self.browser.is_on_page(matchPage.tableGridElement)

    def isVisibleTabs(self) -> bool:
        return self.browser.is_on_page(matchPage.tabs)

    def isVisibleSubTabs(self) -> bool:
        return self.browser.is_on_page(matchPage.subTabs)
