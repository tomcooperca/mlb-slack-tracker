from slack.user import User

def test_init():
    u = User(token='gooblygook', id='ABC123')
    assert u.id == 'ABC123'
