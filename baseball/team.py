from mlbgame import mlbgame
from datetime import datetime

class Team:
    def __init__(self, full_name, abbreviation, location, wins, losses, record,
    division, standing, todays_game_text, todays_game_score):
        self.full_name = full_name
        self.abbreviation = abbreviation
        self.location = location
        self.wins = wins
        self.losses = losses
        self.record = record
        self.division = division
        self.standing = standing
        self.todays_game_text = todays_game_text
        self.todays_game_score = todays_game_score

class TeamMapper:
    def __init__(self, divisions, todays_games, abbreviation=None, full_name=None, location=None):
        self.divisions = divisions
        self.todays_games = todays_games
        self.abbreviation = abbreviation
        self.full_name = full_name
        self.location = location
        self.mlb_team = None

    def log_team_not_found_error(self):
        errors = ""
        if self.abbreviation:
            errors += self.abbreviation
        if self.location:
            errors += "/ {}".format(self.location)
        if self.full_name:
            errors += "/ {}".format(self.full_name)
        print('No team found for {}'.format(errors))


    def list_all_team_abbrevs(self):
        abbrevs = []
        for division in self.divisions:
            for team in division.teams:
                abbrevs.append(team.team_abbrev)
        return abbrevs

    def populate(self):
        self.find_team()
        if self.mlb_team:
            self.populate_team()


    def find_team(self):
        for division in self.divisions:
            for team in division.teams:
                if self.abbreviation and self.abbreviation == team.team_abbrev:
                    self.mlb_team = team
                    self.populate_team()
                elif self.full_name and self.full in team.team_full:
                    self.mlb_team = team
                    self.populate_team()
                elif self.location and self.location in team.team_full:
                    self.mlb_team = team
                    self.populate_team()
                elif self.location and self.location in team.team_short:
                    self.mlb_team = team
                    self.populate_team()
                else:
                    continue


    def find_team_by_name(self, name):
        for division in self.divisions:
            for team in division.teams:
                if name in team.team_full:
                    return team
        return None


    def convert_division_to_short_name(self):
        return (self.mlb_team.division.replace('National League', 'NL')
                                        .replace('American League', 'AL'))


    def correct_for_dbacks(self, game_team_name):
        """
        Arizona Diamondbacks in mlbgame.standings().divisions[...].team_short
        does not match D-backs in GameScoreboards.
        see
        """
        if game_team_name == 'D-backs':
            return 'Diamondbacks'
        return game_team_name


    def find_todays_game_text(self):
        game_text = "Off-Day"
        for game in self.todays_games:
            # GameScoreboard
            if game.home_team in self.mlb_team.team_full:
                real_team_name = self.correct_for_dbacks(game.away_team)
                other_team = self.find_team_by_name(name=real_team_name)
                game_text = self.format_home_team(away_team=other_team.team_abbrev)
            if game.away_team in self.mlb_team.team_full:
                real_team_name = self.correct_for_dbacks(game.home_team)
                other_team = self.find_team_by_name(name=real_team_name)
                game_text = self.format_away_team(home_team=other_team.team_abbrev)
        return game_text


    def find_todays_game_score(self, home_team_name=None, away_team_name=None):
        score = None
        for game in self.todays_games:
            if game.home_team in home_team_name and game.game_status == 'FINAL':
                score = self.format_score(game)
            if game.away_team in away_team_name and game.game_status == 'FINAL':
                score = self.format_score(game)
        return score


    def format_score(self, game):
        return "{}-{}".format(game.away_team_runs, game.home_team_runs)


    def format_home_team(self, away_team):
        return "{}@{}".format(away_team, self.mlb_team.team_abbrev)


    def format_away_team(self, home_team):
        return "{}@{}".format(self.mlb_team.team_abbrev, home_team)


    def populate_team(self):
        self.team = Team(full_name=self.mlb_team.team_full,
                        abbreviation=self.mlb_team.team_abbrev,
                        location=self.mlb_team.team_short,
                        wins=self.mlb_team.w,
                        losses=self.mlb_team.l,
                        record="{}W-{}L".format(self.mlb_team.w, self.mlb_team.l),
                        division=self.convert_division_to_short_name(),
                        standing=self.mlb_team.place,
                        todays_game_text=self.find_todays_game_text(),
                        todays_game_score=self.find_todays_game_score(home_team_name=self.mlb_team.team_full, away_team_name=self.mlb_team.team_full))
