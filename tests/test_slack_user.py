from unittest.mock import MagicMock
from slack.user import User

reusableUser = User(token='blah', id='UB00123')

def test_init():
    u = User(token='gooblygook', id='ABC123')
    assert u.id == 'ABC123'

def test_status_calls_updater():
    reusableUser.su.display_status = MagicMock(return_value="Test status")
    reusableUser.status()
    reusableUser.su.display_status.assert_called_with()

def test_emoji_calls_updater():
    reusableUser.su.display_status_emot = MagicMock(return_value=":cat:")
    reusableUser.emoji()
    reusableUser.su.display_status_emot.assert_called_with()
