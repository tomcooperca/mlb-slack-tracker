from baseball.team import Team
from slack.updater import StatusUpdater
from datetime import datetime

class User():
    def __init__(self, token, id, team=None, created_date=datetime.now()):
        self.token = token
        self.id = id
        self.team = team
        self.created_date = created_date
        self.su = StatusUpdater(id, token)


    def status(self):
        return self.su.display_status()


    def emoji(self):
        return self.su.display_status_emot()

    # Different flavors of status:
    # MYTEAM@OTHER | 1W-2L | 1st in AL East
    def simple_team_and_standings(self):
        # City Name Players | 0W - 0L | AL East
        status = "{} | {} | {}".format(
            self.team.full_name,
            self.team.record,
            self.team.division)
        self.su.update_status(status=status)
