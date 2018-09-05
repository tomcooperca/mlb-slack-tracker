# Slack status updater
# POST's statuses to Slack API
import requests
import json
from urllib.parse import urlencode


class StatusUpdater:

    def __init__(self, id, token, slack_url='https://slack.com/api', ssl_verify=True):
        self.id = id
        self.token = token
        self.slack_url = slack_url
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()
        self.default_headers = {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json'
        }
        self.profile = requests.get('{}/users.profile.get'.format(self.slack_url),
                                headers=self.default_headers, verify=self.ssl_verify).json()


    def update_status(self, status=None):
        current_emot = self.display_status_emot()
        update = {
            'user': self.id,
            'profile': {
                'status_text': status if status else self.display_status(),
                'status_emoji': current_emot
            }
        }
        requests.post('{}/users.profile.set'.format(self.slack_url), data=json.dumps(update),
                                 headers=self.default_headers, verify=self.ssl_verify)

    def display_status_emot(self):
        return self.profile['profile']['status_emoji']

    def display_status(self):
        return self.profile['profile']['status_text']
