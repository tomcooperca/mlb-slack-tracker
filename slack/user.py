from baseball.team import Team
from slack.updater import StatusUpdater
from datetime import datetime

class User():
    def __init__(self, token, id, team):
        self.token = token
        self.id = id
        self.team = team
        self.su = StatusUpdater(id, token)


    def status(self):
        return self.su.display_status()


    def emoji(self):
        return self.su.display_status_emot()


    # Different flavors of status:
    # MYTEAM | 1W-2L
    def simple_team_and_record(self):
        status = "{} | {}".format(self.team.abbreviation, self.team.record)
        self.su.update_status(status=status)


    # MYTEAM@OTHER | 1W-2L | 1st in AL East
    def todays_game_and_standings(self):
        # City Name Players | 0W - 0L | AL East
        status = "{} | {} | #{} in {}".format(
            self.team.todays_game_text,
            self.team.record,
            self.team.standing,
            self.team.division)
        self.su.update_status(status=status)


    def todays_game_score_and_standings(self):
        # TEAM@OTHER (Final: 1-3 is a score exists) | 0W - 0L | #4 in AL East
        score = None
        if self.team.todays_game_score:
            score = "Final: {}".format(self.team.todays_game_score)

        status = "{} {}| {} | #{} in {}".format(
            self.team.todays_game_text,
            "({}) ".format(score) if score else '',
            self.team.record,
            self.team.standing,
            self.team.division)
        self.su.update_status(status=status)
