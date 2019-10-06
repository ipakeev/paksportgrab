from paksportgrab.grabber import Grabber


def test_leagueSeasons(grabber: Grabber):
    seasons = grabber.getSeasons('https://www.oddsportal.com/soccer/europe/euro-2016/results/')
    # current season is first
    assert seasons[0].name == '2016'
    assert seasons[0].url == 'https://www.oddsportal.com/soccer/europe/euro-2016/results/'
    assert seasons[-4].name == '2012'
    assert seasons[-4].url == 'https://www.oddsportal.com/soccer/europe/euro-2012/results/'
