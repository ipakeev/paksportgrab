import re


class ReCompiled:
    date = re.compile(r'(\d\d) (\w\w\w) (\d{4})')
    dateTime = re.compile(r'(\d\d) (\w\w\w) (\d{4}).+?(\d\d:\d\d)')
    oddValue = re.compile(r'([+-]\d[.\d]*$|0$)')


class UserPage:
    loginBtn = 'div.fix > button'
    logoutBtn = '#user-header-logout > a'
    usernameForm = '#login-username1'
    passwordForm = '#login-password1'
    loginFormBtn = '#col-content > div.form > div.content > form > div > button'


class SportPage:
    date = '#col-content > h1'
    currentSport = '#tabdiv_sport > ul > li.tab.active > a'
    moreSport = '#others-link-sport > span'
    currentSortTab = '#tabdiv_sort > ul > li.tab.active > a'
    kickOffTimeTab = '#sort_time > a'
    eventsTab = '#sort_events > a'
    grid = '#table-matches > table > tbody > tr'
    gridElement = '#table-matches > table > tbody > tr.odd'
    error = '#col-content > h1'  # ????


class LeaguePageNavigation:
    currentSeason = '.main-filter .active'
    seasons = '.main-filter > li > span > strong > a'
    currentPage = '#pagination .active-page'
    buttons = '#pagination > a'
    startButton = '|«'
    previousButton = '«'
    nextButton = '»'
    endButton = '»|'


class LeaguePage:
    SCL = '#breadcrumb > a'
    grid = '#tournamentTable > tbody > tr'
    gridElement = '#tournamentTable > tbody .odd'
    ignoreTabs = ['NEXT MATCHES', 'RESULTS', 'STANDINGS', 'OUTRIGHTS']
    navigation = LeaguePageNavigation()


class MatchPage:
    SCL = '#breadcrumb > a'
    teams = '#col-content > h1'
    date = '#col-content > p.date'
    result = '#event-status > p'
    currentTab = '#bettype-tabs > ul > li.active'
    tabs = '#bettype-tabs > ul > li'
    moreTab = '#tab-sport-others > span'
    moreTabsHidden = '#bettype-tabs > ul > li.r.more.hover > div > div > p > a'
    currentSubTab = '#bettype-tabs-scope > ul > li.active'
    subTabs = '#bettype-tabs-scope > ul > li'
    valueGrid = '#odds-data-table > div > div'
    valueGridBorder = '#col-content > div.table-chunk-header-dark > div'
    valueGridElement = '#odds-data-table > div.table-container'
    tableGridBorder = '#odds-data-table > div > table > thead > tr > th.center'
    tableGridElement = '#odds-data-table > div > table > tfoot > tr.aver > td.right'
    tableGridBkNum = '#odds-data-table > div > table > tbody > tr.lo'


class Message:
    msg = '.message-info'  # 'No data available', 'try again' in msg
    internetError = '#main-message > h1 > span'  # 'Нет подключения к Интернету'


reCompiled = ReCompiled()
userPage = UserPage()
sportPage = SportPage()
leaguePage = LeaguePage()
matchPage = MatchPage()
message = Message()
