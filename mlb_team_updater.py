import os
import socket
import sys
from slack.updater import StatusUpdater
TOKEN = os.environ.get('SLACK_TOKEN')
EMAIL = os.environ.get('SLACK_EMAIL')
TEAM = os.environ.get('MLB_TEAM_NAME')


def main():
    if not TOKEN or not EMAIL:
        print("Missing required environment variables. Exiting...")
        sys.exit(1)
    updater = StatusUpdater(token=TOKEN, email=EMAIL)
    updater.update_status(status="Test status update from {}".format(socket.gethostname()))
    print("Status of user {0}: {1}".format(EMAIL, updater.display_status()))
    sys.exit(0)

if __name__ == '__main__':
    main()