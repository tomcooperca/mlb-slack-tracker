import pytest
import mlbgame
from baseball.team import TeamMapper

def test_convert_division_long_name_to_short():
    class DummyTeam():
        def __init__(self, division=None):
            self.division = division

    tf = TeamMapper(divisions=None, todays_games=None)

    dummy = DummyTeam(division='American League')
    tf.mlb_team = dummy
    assert tf.convert_division_to_short_name() == 'AL'

    dummy = DummyTeam(division='National League')
    tf.mlb_team = dummy
    assert tf.convert_division_to_short_name() == 'NL'

    dummy = DummyTeam(division='Baseball League')
    tf.mlb_team = dummy
    assert tf.convert_division_to_short_name() == 'Baseball League'

@pytest.mark.usefixtures("static_standings", "static_games")
def test_game_text_and_score(static_standings, static_games):
    # when
    tf = TeamMapper(divisions=static_standings.divisions, todays_games=static_games, abbreviation='TOR')
    tf.find_team()

    # then
    assert tf.team.todays_game_text == 'TB@TOR'
    assert tf.team.todays_game_score == None
