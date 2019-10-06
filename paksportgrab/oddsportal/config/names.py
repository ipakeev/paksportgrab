sportName = {
    'Soccer': 'soccer',
    'Tennis': 'tennis',
    'Basketball': 'basketball',
    'Hockey': 'hockey',
    'Handball': 'handball',
    'Baseball': 'baseball',
    'American Football': 'american-football',
    'Rugby Union': 'rugby-union',
    'Rugby League': 'rugby-league',
    'Volleyball': 'volleyball',
    'Floorball': 'floorball',
    'Bandy': 'bandy',
    'Futsal': 'futsal',
    'Cricket': 'cricket',
    'Snooker': 'snooker',
    'Darts': 'darts',
    'Boxing': 'boxing',
    'Beach Volleyball': 'beach-volleyball',
    'Aussie Rules': 'aussie-rules',
    'Badminton': 'badminton',
    'Water polo': 'water-polo',
    'Beach Soccer': 'beach-soccer',
    'Pesäpallo': 'pesapallo',
    'eSports': 'esports',
    'MMA': 'mma',
}

WDL = '1X2'
WL = 'home/away'
total = 'total'
handicap = 'handicap'
DNB = 'DNB'
DC = 'DC'
EH = 'EH'
CS = 'CS'
_More = 'More'

tabName = {
    '1X2': WDL,
    'Home/Away': WL,
    'Over/Under': total,
    'O/U': total,
    'Asian Handicap': handicap,
    'AH': handicap,
    'DNB': DNB,
    'Draw No Bet': DNB,
    'DC': DC,
    'Double Chance': DC,
    'EH': EH,
    'European Handicap': EH,
    'CS': CS,
    'Correct Score': CS,
    'More bets': _More,
}

ft = 'ft'
ftot = 'ftot'
h1 = 'I'
h2 = 'II'
h3 = 'III'
q1 = '1q'
q2 = '2q'
q3 = '3q'
q4 = '4q'
subTabName = {
    'Full Time': ft,
    'FT including OT': ftot,
    '1st Half': h1,
    '1st Half Innings': h1,
    '1st Period': h1,
    '2nd Half': h2,
    '2nd Period': h2,
    '3d Period': h3,
    '1Q': q1,
    '1st Inning': q1,
    '2Q': q2,
    '3Q': q3,
    '4Q': q4,
}

matchTableGrid = 'tableGrid'
matchValueGrid = 'valueGrid'

tabs = [WDL, WL, handicap, total]
subTabs = {
    WDL: [ft, h1, q1],
    WL: [ftot, h1, q1],
    handicap: [ftot, ft, h1, q1],
    total: [ftot, ft, h1, q1],
}
tableOrValueGrid = {
    WDL: matchTableGrid,
    WL: matchTableGrid,
    handicap: matchValueGrid,
    total: matchValueGrid,
}

baseUrl = 'https://www.oddsportal.com/'
cancelledTypes = ['award.', 'canc.', 'postp.', 'abn.', 'w.o.', 'int.', 'TF']
cookiePath = './cookies/'
