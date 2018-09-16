import app

def test_find_by_abbreviation():
    app.first_things_first()
    a = 'NYY'
    t = app.find_by_abbreviation(a)
    assert t.abbreviation == 'NYY'


def test_find_by_abbreviation_invalid():
    app.first_things_first()
    a = 'ABC'
    assert app.find_by_abbreviation(a) == None
