from baseball.team import Team

class User():
    def __init__(self, email, team=Team('NYY'), created_date,  token):
        self.email = email
        self.team = team
        self.created_date = created_date
        self.token = token
        self.su = StatusUpdater(email, token)


    def status(self):
        return su.display_status()


    def emoji(self):
        return su.display_status_emot()
