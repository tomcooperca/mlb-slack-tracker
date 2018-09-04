# Represents an MLB team, with current state of its games, standings, etc.
class Team:
    def __init__(self, name):
        self.name = name
        self.divisions = mlbgame.standings().divisions
        abbrevs = []
        for division in self.divisions:
            for team in division.teams:
                abbrevs.append(team.team_abbrev)
        self.abbrevs = abbrevs

    def find_team_by_abbrev(self, abbrev):
        for division in self.divisions:
            for team in division.teams:
                if team.team_abbrev == abbrev:
                    return team
        return None


    def find_team_by_full_name(self, full_name):
        for division in self.divisions:
            for team in division.teams:
                if team.team_full == full_name:
                    return team
        return None


    def find_team_by_name(self, name):
        for division in self.divisions:
            for team in division.teams:
                if name in team.team_full:
                    return team
        return None


    def find_divison_by_abbrev(self, abbrev):
        for division in self.divisions:
            for team in division.teams:
                if team.team_abbrev == abbrev:
                    return division
        return None


    def valid_team(self, abbrev):
        found_team = False
        for division in self.divisions:
            for team in division.teams:
                if team.team_abbrev == abbrev:
                    found_team = True
        return found_team
