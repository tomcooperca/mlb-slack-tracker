from unittest.mock import MagicMock
import mlbgame
from baseball.team import TeamMapper
import datetime

def test_convert_division_long_name_to_short():
    class DummyTeam():
        def __init__(self, division=None):
            self.division = division

    tf = TeamMapper(divisions=None)

    dummy = DummyTeam(division='American League')
    tf.mlb_team = dummy
    assert tf.convert_division_to_short_name() == 'AL'

    dummy = DummyTeam(division='National League')
    tf.mlb_team = dummy
    assert tf.convert_division_to_short_name() == 'NL'

    dummy = DummyTeam(division='Baseball League')
    tf.mlb_team = dummy
    assert tf.convert_division_to_short_name() == 'Baseball League'


def test_game_text_and_score():
# TODO: figure out a good way to fixture mlbgame.standings().divisions and mlbgame.day(today).games
    # tf = TeamMapper(divisions=mlbgame.mlbgame.standings().divisions, abbreviation='TOR')
#     tf.todays_games = Fixtures.GAMES_FIXTURE
#     mocked_team = MagicMock()
#     mocked_team.team_abbrev = MagicMock(return_value='TOR')
#     mocked_team.team_full = MagicMock(return_value='Toronto Blue Jays')
#     tf.mlb_game = mocked_team

    # tf.find_team()
    # assert tf.team.todays_game_text == 'TOR@BAL'
    # assert tf.team.todays_game_score == None
