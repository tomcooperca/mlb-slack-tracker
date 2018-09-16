# Slack status updater
# POST's statuses to Slack API
import requests
import json
from urllib.parse import urlencode
from datetime import datetime, timezone, timedelta

class StatusUpdater:

    def __init__(self, id, token, slack_url='https://slack.com/api', ssl_verify=True):
        self.id = id
        self.token = token
        self.slack_url = slack_url
        self.ssl_verify = ssl_verify
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()
        self.default_headers = {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json',
            'X-Slack-User': id
        }


    def update_status(self, status=None):
        print("Updating status of {} to \"{}\"".format(self.id, status))
        current_emot = self.display_status_emot()
        today_utc = datetime.now().replace(tzinfo=timezone.utc)
        next_week_timestamp = int((today_utc + timedelta(days=7)).timestamp())
        update = {
            'profile': {
                'status_text': status if status else self.display_status(),
                'status_emoji': current_emot,
                'status_expiration': '{}'.format(next_week_timestamp)
            }
        }
        response = requests.post('{}/users.profile.set'.format(self.slack_url), data=json.dumps(update),
                                 headers=self.default_headers, verify=self.ssl_verify)
        print(response.status_code)
        print(response.text)


    def display_status_emot(self):
        return self.get_profile()['profile']['status_emoji']

    def display_status(self):
        return self.get_profile()['profile']['status_text']

    def display_email(self):
        return self.get_profile()['profile']['email']

    def get_profile(self):
        return requests.get('{}/users.profile.get'.format(self.slack_url),
                                headers=self.default_headers, verify=self.ssl_verify).json()
