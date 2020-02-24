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
    MoreBets = 'More'
    BTS = 'BTS'
    OE = 'OE'
    TQ = 'TQ'


class subTab:
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


sportName = {
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

tabName = {
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
    'More bets': tab.MoreBets,
    'BTS': tab.BTS,
    'Both Teams to Score': tab.BTS,
    'O/E': tab.OE,
    'Odd or Even': tab.OE,
    'TQ': tab.TQ,
    'To Qualify': tab.TQ,
}

subTabName = {
    'Full Time': subTab.ft,
    'FT including OT': subTab.ftot,
    '1st Half': subTab.h1,
    '1st Half Innings': subTab.h1,
    '1st Period': subTab.h1,
    '2nd Half': subTab.h2,
    '2nd Half Innings': subTab.h2,
    '2nd Period': subTab.h2,
    '3rd Period': subTab.h3,
    '1Q': subTab.q1,
    '1st Inning': subTab.q1,
    '2Q': subTab.q2,
    '3Q': subTab.q3,
    '4Q': subTab.q4,
}

sportTabs = {
    sport.soccer: {
        tab.WDL: [subTab.ft, subTab.h1],
        tab.handicap: [subTab.ft],
        tab.total: [subTab.ft, subTab.h1],
    },
    sport.hockey: {
        tab.WDL: [subTab.ft, subTab.h1],
        tab.WL: [subTab.ftot],
        tab.handicap: [subTab.ftot, subTab.ft],
        tab.total: [subTab.ftot, subTab.ft, subTab.h1],
    },
    sport.basketball: {
        tab.WL: [subTab.ftot],
        tab.handicap: [subTab.ftot],
        tab.total: [subTab.ftot, subTab.ft, subTab.h1, subTab.q1],
    },
    sport.baseball: {
        tab.WL: [subTab.ftot],
        tab.handicap: [subTab.ftot],
        tab.total: [subTab.ftot, subTab.h1, subTab.q1],
    },
}

matchTableGrid = 'tableGrid'
matchValueGrid = 'valueGrid'

tableOrValueGrid = {
    tab.WDL: matchTableGrid,
    tab.WL: matchTableGrid,
    tab.handicap: matchValueGrid,
    tab.total: matchValueGrid,
}

baseUrl = 'https://www.oddsportal.com/'
cancelledTypes = ['award.', 'canc.', 'postp.', 'abn.', 'w.o.', 'int.', 'TF']
cookiePath = './cookies/'

train = 'train'
test = 'test'
val = 'val'
ttv = ['train', 'test', 'val']
test_val = ['test', 'val']
