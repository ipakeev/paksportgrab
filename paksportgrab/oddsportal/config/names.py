class sport:
    soccer = 'soccer'
    tennis = 'tennis'
    basketball = 'basketball'
    hockey = 'hockey'
    handball = 'handball'
    baseball = 'baseball'
    american_football = 'american-football'
    rugby_union = 'rugby-union'
    rugby_league = 'rugby-league'
    volleyball = 'volleyball'
    floorball = 'floorball'
    bandy = 'bandy'
    futsal = 'futsal'
    cricket = 'cricket'
    snooker = 'snooker'
    darts = 'darts'
    boxing = 'boxing'
    beach_volleyball = 'beach-volleyball'
    aussie_rules = 'aussie-rules'
    badminton = 'badminton'
    water_polo = 'water-polo'
    beach_soccer = 'beach-soccer'
    pesapallo = 'pesapallo'
    esports = 'esports'
    mma = 'mma'


class tab:
    WDL = '1X2'
    WL = 'home/away'
    total = 'total'
    handicap = 'handicap'
    DNB = 'DNB'
    DC = 'DC'
    EH = 'EH'
    HTFT = 'HTFT'
    CS = 'CS'
    more_bets = 'More'
    BTS = 'BTS'
    OE = 'OE'
    TQ = 'TQ'


class sub_tab:
    ft = 'ft'
    ftot = 'ftot'
    ot = 'ot'
    innings = 'innings'
    h1 = 'I'
    h2 = 'II'
    h3 = 'III'
    q1 = '1q'
    q2 = '2q'
    q3 = '3q'
    q4 = '4q'


class tip:
    W1 = 'W1'
    WX = 'WX'
    W2 = 'W2'
    DNB1 = 'DNB1'
    DNB2 = 'DNB2'
    DC1X = 'DC1X'
    DCX2 = 'DCX2'
    DC12 = 'DC12'
    AH1 = 'AH1'
    AH2 = 'AH2'
    over = 'over'
    under = 'under'


sport_name = {
    'Soccer': sport.soccer,
    'Tennis': sport.tennis,
    'Basketball': sport.basketball,
    'Hockey': sport.hockey,
    'Handball': sport.handball,
    'Baseball': sport.baseball,
    'American Football': sport.american_football,
    'Rugby Union': sport.rugby_union,
    'Rugby League': sport.rugby_league,
    'Volleyball': sport.volleyball,
    'Floorball': sport.floorball,
    'Bandy': sport.bandy,
    'Futsal': sport.futsal,
    'Cricket': sport.cricket,
    'Snooker': sport.snooker,
    'Darts': sport.darts,
    'Boxing': sport.boxing,
    'Beach Volleyball': sport.beach_volleyball,
    'Aussie Rules': sport.aussie_rules,
    'Badminton': sport.badminton,
    'Water polo': sport.water_polo,
    'Beach Soccer': sport.beach_soccer,
    'Pesäpallo': sport.pesapallo,
    'eSports': sport.esports,
    'MMA': sport.mma,
}

tab_name = {
    '1X2': tab.WDL,
    'Home/Away': tab.WL,
    'O/U': tab.total,
    'Over/Under': tab.total,
    'AH': tab.handicap,
    'Asian Handicap': tab.handicap,
    'DNB': tab.DNB,
    'Draw No Bet': tab.DNB,
    'DC': tab.DC,
    'Double Chance': tab.DC,
    'EH': tab.EH,
    'European Handicap': tab.EH,
    'HT/FT': tab.HTFT,
    'Half Time / Full Time': tab.HTFT,
    'CS': tab.CS,
    'Correct Score': tab.CS,
    'More bets': tab.more_bets,
    'BTS': tab.BTS,
    'Both Teams to Score': tab.BTS,
    'O/E': tab.OE,
    'Odd or Even': tab.OE,
    'TQ': tab.TQ,
    'To Qualify': tab.TQ,
}

sub_tab_name = {
    'Full Time': sub_tab.ft,
    'FT including OT': sub_tab.ftot,
    '1st Half': sub_tab.h1,
    '1st Half Innings': sub_tab.h1,
    '1st Period': sub_tab.h1,
    '2nd Half': sub_tab.h2,
    '2nd Half Innings': sub_tab.h2,
    '2nd Period': sub_tab.h2,
    '3rd Period': sub_tab.h3,
    '1Q': sub_tab.q1,
    '1st Inning': sub_tab.q1,
    '2Q': sub_tab.q2,
    '3Q': sub_tab.q3,
    '4Q': sub_tab.q4,
}

sport_tabs = {
    sport.soccer: {
        tab.WDL: [sub_tab.ft, sub_tab.h1],
        tab.handicap: [sub_tab.ft],
        tab.total: [sub_tab.ft, sub_tab.h1],
    },
    sport.hockey: {
        tab.WDL: [sub_tab.ft, sub_tab.h1],
        tab.WL: [sub_tab.ftot],
        tab.handicap: [sub_tab.ftot, sub_tab.ft],
        tab.total: [sub_tab.ftot, sub_tab.ft, sub_tab.h1],
    },
    sport.basketball: {
        tab.WL: [sub_tab.ftot],
        tab.handicap: [sub_tab.ftot],
        tab.total: [sub_tab.ftot, sub_tab.ft, sub_tab.h1, sub_tab.q1],
    },
    sport.baseball: {
        tab.WL: [sub_tab.ftot],
        tab.handicap: [sub_tab.ftot],
        tab.total: [sub_tab.ftot, sub_tab.h1, sub_tab.q1],
    },
}

match_table_grid = 'tableGrid'
match_value_grid = 'valueGrid'

tableOrValueGrid = {
    tab.WDL: match_table_grid,
    tab.WL: match_table_grid,
    tab.handicap: match_value_grid,
    tab.total: match_value_grid,
}

base_url = 'https://www.oddsportal.com/'
cancelled_types = ['award.', 'canc.', 'postp.', 'abn.', 'w.o.', 'int.', 'TF']
cookie_path = './cookies/'

train = 'train'
test = 'test'
val = 'val'
ttv = ['train', 'test', 'val']
test_val = ['test', 'val']
