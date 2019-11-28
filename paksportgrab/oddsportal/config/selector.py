import re
from selenium.webdriver.common.by import By


class ReCompiled:
    date = re.compile(r'(\d\d) (\w\w\w) (\d{4})')
    dateTime = re.compile(r'(\d\d) (\w\w\w) (\d{4}).+?(\d\d:\d\d)')
    oddValue = re.compile(r'([+-]\d[.\d]*$|0$)')


class UserPage:
    loginBtn = (By.CSS_SELECTOR, 'div.fix > button')
    logoutBtn = (By.CSS_SELECTOR, '#user-header-logout > a')
    usernameForm = (By.CSS_SELECTOR, '#login-username1')
    passwordForm = (By.CSS_SELECTOR, '#login-password1')
    loginFormBtn = (By.CSS_SELECTOR, '#col-content > div.form > div.content > form > div > button')


class SportPage:
    date = (By.CSS_SELECTOR, '#col-content > h1')
    currentSport = (By.CSS_SELECTOR, '#tabdiv_sport > ul > li.tab.active > a')
    moreSport = (By.CSS_SELECTOR, '#others-link-sport > span')
    currentSortTab = (By.CSS_SELECTOR, '#tabdiv_sort > ul > li.tab.active > a')
    kickOffTimeTab = (By.CSS_SELECTOR, '#sort_time > a')
    eventsTab = (By.CSS_SELECTOR, '#sort_events > a')
    grid = (By.CSS_SELECTOR, '#table-matches > table > tbody > tr')
    gridElement = (By.CSS_SELECTOR, '#table-matches > table > tbody > tr.odd')
    error = (By.CSS_SELECTOR, '#col-content > h1')  # ????


class LeaguePageNavigation:
    currentSeason = (By.CSS_SELECTOR, '.main-filter .active')
    seasons = (By.CSS_SELECTOR, '.main-filter > li > span > strong > a')
    currentPage = (By.CSS_SELECTOR, '#pagination .active-page')
    buttons = (By.CSS_SELECTOR, '#pagination > a')
    startButton = '|«'
    previousButton = '«'
    nextButton = '»'
    endButton = '»|'


class LeaguePage:
    SCL = (By.CSS_SELECTOR, '#breadcrumb > a')
    grid = (By.CSS_SELECTOR, '#tournamentTable > tbody > tr')
    gridElement = (By.CSS_SELECTOR, '#tournamentTable > tbody .odd')
    ignoreTabs = ['NEXT MATCHES', 'RESULTS', 'STANDINGS', 'OUTRIGHTS']
    navigation = LeaguePageNavigation()


class MatchPage:
    SCL = (By.CSS_SELECTOR, '#breadcrumb > a')
    teams = (By.CSS_SELECTOR, '#col-content > h1')
    date = (By.CSS_SELECTOR, '#col-content > p.date')
    result = (By.CSS_SELECTOR, '#event-status > p')
    currentTab = (By.CSS_SELECTOR, '#bettype-tabs > ul > li.active')
    tabs = (By.CSS_SELECTOR, '#bettype-tabs > ul > li')
    moreTab = (By.CSS_SELECTOR, '#tab-sport-others > span')
    moreTabsHidden = (By.CSS_SELECTOR, '#bettype-tabs > ul > li.r.more.hover > div > div > p > a')
    currentSubTab = (By.CSS_SELECTOR, '#bettype-tabs-scope > ul > li.active')
    subTabs = (By.CSS_SELECTOR, '#bettype-tabs-scope > ul > li')
    valueGrid = (By.CSS_SELECTOR, '#odds-data-table > div > div')
    valueGridBorder = (By.CSS_SELECTOR, '#col-content > div.table-chunk-header-dark > div')
    valueGridElement = (By.CSS_SELECTOR, '#odds-data-table > div.table-container')
    tableGridBorder = (By.CSS_SELECTOR, '#odds-data-table > div > table > thead > tr > th.center')
    tableGridElement = (By.CSS_SELECTOR, '#odds-data-table > div > table > tfoot > tr.aver > td.right')
    tableGridBkNum = (By.CSS_SELECTOR, '#odds-data-table > div > table > tbody > tr.lo')


class Message:
    msg = (By.CSS_SELECTOR, '.message-info')  # 'No data available', 'try again' in msg
    internetError = (By.CSS_SELECTOR, '#main-message > h1 > span')  # 'Нет подключения к Интернету'


reCompiled = ReCompiled()
userPage = UserPage()
sportPage = SportPage()
leaguePage = LeaguePage()
matchPage = MatchPage()
message = Message()
