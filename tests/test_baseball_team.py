from baseball.team import TeamFinder

def test_convert_division_long_name_to_short():
    class DummyTeam():
        def __init__(self, division=None):
            self.division = division

    tf = TeamFinder(divisions=None)

    dummy = DummyTeam(division='American League')
    tf.mlb_team = dummy
    assert tf.convert_division_to_short_name() == 'AL'

    dummy = DummyTeam(division='National League')
    tf.mlb_team = dummy
    assert tf.convert_division_to_short_name() == 'NL'

    dummy = DummyTeam(division='Baseball League')
    tf.mlb_team = dummy
    assert tf.convert_division_to_short_name() == 'Baseball League'
