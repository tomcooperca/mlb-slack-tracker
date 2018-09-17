import mlbgame

class Team:
    def __init__(self, full_name, abbreviation, location, wins, losses, record, division, standing):
        self.full_name = full_name
        self.abbreviation = abbreviation
        self.location = location
        self.wins = wins
        self.losses = losses
        self.record = record
        self.division = division
        self.standing = standing

class TeamFinder:
    def __init__(self, divisions, abbreviation=None, full_name=None, location=None):
        self.abbreviation = abbreviation
        self.full_name = full_name
        self.location = location
        self.divisions = divisions
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
        find_team(self)
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


    def convert_division_to_short_name(self):
        return (self.mlb_team.division.replace('National League', 'NL')
                       .replace('American League', 'AL'))


    def populate_team(self):
        self.team = Team(full_name=self.mlb_team.team_full,
                        abbreviation=self.mlb_team.team_abbrev,
                        location=self.mlb_team.team_short,
                        wins=self.mlb_team.w,
                        losses=self.mlb_team.l,
                        record="{}W-{}L".format(self.mlb_team.w, self.mlb_team.l),
                        division=self.convert_division_to_short_name(),
                        standing=self.mlb_team.place)
