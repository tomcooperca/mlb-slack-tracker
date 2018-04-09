import datetime
import os
import sys
from slack.updater import StatusUpdater
import mlbgame
TOKEN = os.environ.get('SLACK_TOKEN')
EMAIL = os.environ.get('SLACK_EMAIL')
TEAM = os.environ.get('MLB_TEAM')


def find_team_by_abbrev(divisions, abbrev):
    for division in divisions:
        for team in division.teams:
            if team.team_abbrev == abbrev:
                return team


def find_team_by_full_name(divisions, full_name):
    for division in divisions:
        for team in division.teams:
            if team.team_full == full_name:
                return team


def find_team_by_name(divisions, name):
    for division in divisions:
        for team in division.teams:
            if name in team.team_full:
                return team


def find_divison_by_abbrev(divisions, abbrev):
    for division in divisions:
        for team in division.teams:
            if team.team_abbrev == abbrev:
                return division


def valid_team(divisions, abbrev):
    found_team = False
    for division in divisions:
        for team in division.teams:
            if team.team_abbrev == abbrev:
                found_team = True
    return found_team


def list_all_team_abbrevs(divisions):
    abbrevs = []
    for division in divisions:
        for team in division.teams:
            abbrevs.append(team.team_abbrev)
    return abbrevs


def main():
    if not TOKEN or not EMAIL or not TEAM:
        print("Missing required environment variables. \nRequired:\n\tSLACK_TOKEN\tSLACK_EMAIL\tMLB_TEAM\n\nExiting...")
        sys.exit(1)

    saved_divisions = mlbgame.standings().divisions
    if not valid_team(saved_divisions, TEAM):
        print("Invalid MLB_TEAM value.\nValid values: {}".format(list_all_team_abbrevs(saved_divisions)))
        sys.exit(1)

    found_division = find_divison_by_abbrev(saved_divisions, TEAM)
    found_team = find_team_by_abbrev(saved_divisions, TEAM)
    today = datetime.datetime.now()
    todays_games = mlbgame.day(today.year, today.month, today.day)
    today_game_status = None
    for game in todays_games:
        if game.away_team in found_team.team_full:
            today_game_status = '{}@{}'.format(TEAM, find_team_by_name(saved_divisions, game.home_team).team_abbrev)
        if game.home_team in found_team.team_full:
            today_game_status = '{}@{}'.format(find_team_by_name(saved_divisions, game.away_team).team_abbrev, TEAM)

    if not today_game_status:
        final_status = "Off-Day | {}W - {}L | #{} in {}".format(found_team.w, found_team.l, found_team.place,
                                                                found_division.name)
    else:
        final_status = "{} | {}W - {}L | #{} in {}".format(today_game_status, found_team.w, found_team.l,
                                                           found_team.place, found_division.name)

    updater = StatusUpdater(token=TOKEN, email=EMAIL)
    updater.update_status(status=final_status)
    print("Status of user {0} updated to \"{1}\"".format(EMAIL, updater.display_status()))
    sys.exit(0)


if __name__ == '__main__':
    main()
