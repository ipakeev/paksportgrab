import re

from pakselenium import Selector, By


class ReCompiled:
    date = re.compile(r'(\d\d) (\w+?) (\d{4})')
    date_time = re.compile(r'(\d\d) (\w+?) (\d{4}).+?(\d\d:\d\d)')
    odd_value = re.compile(r'([+-]?\d[.\d]*$)')


class UserPage:
    login_btn = Selector(By.CSS_SELECTOR, 'div.fix > button')
    logout_btn = Selector(By.CSS_SELECTOR, '#user-header-logout > a')
    username_form = Selector(By.CSS_SELECTOR, '#login-username1')
    password_form = Selector(By.CSS_SELECTOR, '#login-password1')
    login_form_btn = Selector(By.CSS_SELECTOR, '#col-content > div.form > div.content > form > div > button')


class SportPage:
    date = Selector(By.CSS_SELECTOR, '#col-content > h1')
    current_sport = Selector(By.CSS_SELECTOR, '#tabdiv_sport > ul > li.tab.active > a')
    more_sport = Selector(By.CSS_SELECTOR, '#others-link-sport > span')
    current_sort_tab = Selector(By.CSS_SELECTOR, '#tabdiv_sort > ul > li.tab.active > a')
    kick_off_time_tab = Selector(By.CSS_SELECTOR, '#sort_time > a')
    events_tab = Selector(By.CSS_SELECTOR, '#sort_events > a')
    grid = Selector(By.CSS_SELECTOR, '#table-matches > table > tbody > tr')
    grid_element = Selector(By.CSS_SELECTOR, '#table-matches > table > tbody > tr > td.table-time')
    error = Selector(By.CSS_SELECTOR, '#col-content > h1')  # ????


class LeaguePageNavigation:
    current_season = Selector(By.CSS_SELECTOR, '.main-filter .active')
    seasons = Selector(By.CSS_SELECTOR, '.main-filter > li > span > strong > a')
    current_page = Selector(By.CSS_SELECTOR, '#pagination .active-page')
    buttons = Selector(By.CSS_SELECTOR, '#pagination > a')
    start_button = '|«'
    previous_button = '«'
    next_button = '»'
    end_button = '»|'


class LeaguePage:
    SCL = Selector(By.CSS_SELECTOR, '#breadcrumb > a')
    grid = Selector(By.CSS_SELECTOR, '#tournamentTable > tbody > tr')
    grid_element = Selector(By.CSS_SELECTOR, '#tournamentTable > tbody .odd')
    ignore_tabs = ['NEXT MATCHES', 'RESULTS', 'STANDINGS', 'OUTRIGHTS']
    navigation = LeaguePageNavigation()


class MatchPage:
    SCL = Selector(By.CSS_SELECTOR, '#breadcrumb > a')
    teams = Selector(By.CSS_SELECTOR, '#col-content > h1')
    date = Selector(By.CSS_SELECTOR, '#col-content > p.date')
    result = Selector(By.CSS_SELECTOR, '#event-status > p')
    current_tab = Selector(By.CSS_SELECTOR, '#bettype-tabs > ul > li.active')
    tabs = Selector(By.CSS_SELECTOR, '#bettype-tabs > ul > li')
    more_tab = Selector(By.CSS_SELECTOR, '#tab-sport-others > span')
    more_tabs_hidden = Selector(By.CSS_SELECTOR, '#bettype-tabs > ul > li.r.more.hover > div > div > p > a')
    current_sub_tab = Selector(By.CSS_SELECTOR, '#bettype-tabs-scope > ul > li.active')
    sub_tabs = Selector(By.CSS_SELECTOR, '#bettype-tabs-scope > ul > li')
    value_grid = Selector(By.CSS_SELECTOR, '#odds-data-table > div > div')
    value_grid_border = Selector(By.CSS_SELECTOR, '#col-content > div.table-chunk-header-dark > div')
    value_grid_element = Selector(By.CSS_SELECTOR, '#odds-data-table > div.table-container')
    table_grid_border = Selector(By.CSS_SELECTOR, '#odds-data-table > div > table > thead > tr > th.center')
    table_grid_element = Selector(By.CSS_SELECTOR, '#odds-data-table > div > table > tfoot > tr.aver > td.right')
    table_grid_bk_num = Selector(By.CSS_SELECTOR, '#odds-data-table > div > table > tbody > tr.lo')


class Message:
    msg = Selector(By.CSS_SELECTOR, '.message-info')  # 'No data available', 'try again' in msg
    internet_error = Selector(By.CSS_SELECTOR, '#main-message > h1 > span')  # 'Нет подключения к Интернету'


re_compiled = ReCompiled()
user_page = UserPage()
sport_page = SportPage()
league_page = LeaguePage()
match_page = MatchPage()
message = Message()
