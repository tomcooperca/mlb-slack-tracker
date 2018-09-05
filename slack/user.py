from baseball.team import Team

class User():
    def __init__(self, token, id, email='inbox@example.com', team=Team('NYY'), created_date=None):
        self.token = token
        self.id = id
        self.email = email
        self.team = team
        self.created_date = created_date
        self.su = StatusUpdater(id, token)


    def status(self):
        return su.display_status()


    def emoji(self):
        return su.display_status_emot()
