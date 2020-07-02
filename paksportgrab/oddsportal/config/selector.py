import re

from pakselenium import Selector, By


class ReCompiled:
    date = re.compile(r'(\d\d) (\w+?) (\d{4})')
    dateTime = re.compile(r'(\d\d) (\w+?) (\d{4}).+?(\d\d:\d\d)')
    oddValue = re.compile(r'([+-]?\d[.\d]*$)')


class UserPage:
    loginBtn = Selector(By.CSS_SELECTOR, 'div.fix > button')
    logoutBtn = Selector(By.CSS_SELECTOR, '#user-header-logout > a')
    usernameForm = Selector(By.CSS_SELECTOR, '#login-username1')
    passwordForm = Selector(By.CSS_SELECTOR, '#login-password1')
    loginFormBtn = Selector(By.CSS_SELECTOR, '#col-content > div.form > div.content > form > div > button')


class SportPage:
    date = Selector(By.CSS_SELECTOR, '#col-content > h1')
    currentSport = Selector(By.CSS_SELECTOR, '#tabdiv_sport > ul > li.tab.active > a')
    moreSport = Selector(By.CSS_SELECTOR, '#others-link-sport > span')
    currentSortTab = Selector(By.CSS_SELECTOR, '#tabdiv_sort > ul > li.tab.active > a')
    kickOffTimeTab = Selector(By.CSS_SELECTOR, '#sort_time > a')
    eventsTab = Selector(By.CSS_SELECTOR, '#sort_events > a')
    grid = Selector(By.CSS_SELECTOR, '#table-matches > table > tbody > tr')
    gridElement = Selector(By.CSS_SELECTOR, '#table-matches > table > tbody > tr > td.table-time')
    error = Selector(By.CSS_SELECTOR, '#col-content > h1')  # ????


class LeaguePageNavigation:
    currentSeason = Selector(By.CSS_SELECTOR, '.main-filter .active')
    seasons = Selector(By.CSS_SELECTOR, '.main-filter > li > span > strong > a')
    currentPage = Selector(By.CSS_SELECTOR, '#pagination .active-page')
    buttons = Selector(By.CSS_SELECTOR, '#pagination > a')
    startButton = '|«'
    previousButton = '«'
    nextButton = '»'
    endButton = '»|'


class LeaguePage:
    SCL = Selector(By.CSS_SELECTOR, '#breadcrumb > a')
    grid = Selector(By.CSS_SELECTOR, '#tournamentTable > tbody > tr')
    gridElement = Selector(By.CSS_SELECTOR, '#tournamentTable > tbody .odd')
    ignoreTabs = ['NEXT MATCHES', 'RESULTS', 'STANDINGS', 'OUTRIGHTS']
    navigation = LeaguePageNavigation()


class MatchPage:
    SCL = Selector(By.CSS_SELECTOR, '#breadcrumb > a')
    teams = Selector(By.CSS_SELECTOR, '#col-content > h1')
    date = Selector(By.CSS_SELECTOR, '#col-content > p.date')
    result = Selector(By.CSS_SELECTOR, '#event-status > p')
    currentTab = Selector(By.CSS_SELECTOR, '#bettype-tabs > ul > li.active')
    tabs = Selector(By.CSS_SELECTOR, '#bettype-tabs > ul > li')
    moreTab = Selector(By.CSS_SELECTOR, '#tab-sport-others > span')
    moreTabsHidden = Selector(By.CSS_SELECTOR, '#bettype-tabs > ul > li.r.more.hover > div > div > p > a')
    currentSubTab = Selector(By.CSS_SELECTOR, '#bettype-tabs-scope > ul > li.active')
    subTabs = Selector(By.CSS_SELECTOR, '#bettype-tabs-scope > ul > li')
    valueGrid = Selector(By.CSS_SELECTOR, '#odds-data-table > div > div')
    valueGridBorder = Selector(By.CSS_SELECTOR, '#col-content > div.table-chunk-header-dark > div')
    valueGridElement = Selector(By.CSS_SELECTOR, '#odds-data-table > div.table-container')
    tableGridBorder = Selector(By.CSS_SELECTOR, '#odds-data-table > div > table > thead > tr > th.center')
    tableGridElement = Selector(By.CSS_SELECTOR, '#odds-data-table > div > table > tfoot > tr.aver > td.right')
    tableGridBkNum = Selector(By.CSS_SELECTOR, '#odds-data-table > div > table > tbody > tr.lo')


class Message:
    msg = Selector(By.CSS_SELECTOR, '.message-info')  # 'No data available', 'try again' in msg
    internetError = Selector(By.CSS_SELECTOR, '#main-message > h1 > span')  # 'Нет подключения к Интернету'


reCompiled = ReCompiled()
userPage = UserPage()
sportPage = SportPage()
leaguePage = LeaguePage()
matchPage = MatchPage()
message = Message()
