import datetime
import os
import sys
from slack.updater import StatusUpdater
import mlbgame
TOKEN = os.environ.get('SLACK_TOKEN')
EMAIL = os.environ.get('SLACK_EMAIL')
TEAM = os.environ.get('MLB_TEAM')


def main():

    today = datetime.datetime.now()

    print("League\tDivision\tTeam\tW\tL\tPlace")
    for division in mlbgame.standings().divisions:
        league = division.name.split(" ")[0]
        region = division.name.split(" ")[1]
        for team in division.teams:
            if team.team_abbrev == TEAM:
                found_division = division
                found_team = team
            print("{}\t{}\t{}\t{}\t{}\t{}".format(
                league, region, team.team_abbrev, team.w, team.l, team.place
            ))

    # TODO check todays games, find matching team and display either "v. <away team>" or "@<home team>"
    todays_games = mlbgame.day(today.year, today.month, today.day)

    if not TOKEN or not EMAIL:
        print("Missing required environment variables. Exiting...")
        sys.exit(1)
    updater = StatusUpdater(token=TOKEN, email=EMAIL)
    updater.update_status(status="{} | {}W - {}L | #{} in {}".format("@TEX", found_team.w, found_team.l,
                                                                     found_team.place, found_division.name))
    print("Status of user {0}: {1}".format(EMAIL, updater.display_status()))
    sys.exit(0)


if __name__ == '__main__':
    main()
