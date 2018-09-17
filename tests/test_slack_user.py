from unittest.mock import MagicMock
from slack.user import User
from baseball.team import Team

reusableUser = User(token='blah', id='UB00123', team=None)
testTeam = Team(abbreviation='CN', location='City Name',
    full_name='City Name Players', record='0W-162L', division='CL Beast',
    wins=0, losses=162, standing=5)

def test_init():
    u = User(token='gooblygook', id='ABC123', team=None)
    assert u.id == 'ABC123'

def test_status_calls_updater():
    reusableUser.su.display_status = MagicMock(return_value="Test status")
    reusableUser.status()
    reusableUser.su.display_status.assert_called_with()

def test_emoji_calls_updater():
    reusableUser.su.display_status_emot = MagicMock(return_value=":cat:")
    reusableUser.emoji()
    reusableUser.su.display_status_emot.assert_called_with()

def test_simple_team_and_standings_status():
    expected = 'City Name Players | 0W-162L | CL Beast'
    u = User(token='blah', id='UB00123', team=testTeam)
    u.su.update_status = MagicMock()

    u.simple_team_and_standings()

    u.su.update_status.assert_called_once_with(status=expected)
