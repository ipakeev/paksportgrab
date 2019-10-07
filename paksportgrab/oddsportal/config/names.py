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

sportName = {
    'Soccer': soccer,
    'Tennis': tennis,
    'Basketball': basketball,
    'Hockey': hockey,
    'Handball': handball,
    'Baseball': baseball,
    'American Football': american_football,
    'Rugby Union': rugby_union,
    'Rugby League': rugby_league,
    'Volleyball': volleyball,
    'Floorball': floorball,
    'Bandy': bandy,
    'Futsal': futsal,
    'Cricket': cricket,
    'Snooker': snooker,
    'Darts': darts,
    'Boxing': boxing,
    'Beach Volleyball': beach_volleyball,
    'Aussie Rules': aussie_rules,
    'Badminton': badminton,
    'Water polo': water_polo,
    'Beach Soccer': beach_soccer,
    'Pesäpallo': pesapallo,
    'eSports': esports,
    'MMA': mma,
}

WDL = '1X2'
WL = 'home/away'
total = 'total'
handicap = 'handicap'
DNB = 'DNB'
DC = 'DC'
EH = 'EH'
CS = 'CS'
MoreBets = 'More'

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
    'More bets': MoreBets,
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

tabs = {
    soccer: {
        WDL: [ft, h1],
        handicap: [ft, h1],
        total: [ft, h1],
    },
    hockey: {
        WDL: [ft, h1],
        WL: [ftot],
        handicap: [ftot, ft],
        total: [ftot, ft, h1],
    },
    basketball: {
        WL: [ftot],
        handicap: [ftot],
        total: [ftot, ft, h1, q1],
    },
    baseball: {
        WL: [ftot],
        handicap: [ftot, h1],
        total: [ftot, h1, q1],
    },
}

matchTableGrid = 'tableGrid'
matchValueGrid = 'valueGrid'

tableOrValueGrid = {
    WDL: matchTableGrid,
    WL: matchTableGrid,
    handicap: matchValueGrid,
    total: matchValueGrid,
}

baseUrl = 'https://www.oddsportal.com/'
cancelledTypes = ['award.', 'canc.', 'postp.', 'abn.', 'w.o.', 'int.', 'TF']
cookiePath = './cookies/'
