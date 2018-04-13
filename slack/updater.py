import requests
import json
from urllib.parse import urlencode


class StatusUpdater:

    def __init__(self, token='', email='example@email.com', ssl_verify=True):
        if not ssl_verify:
            requests.packages.urllib3.disable_warnings()
        self.ssl_verify = ssl_verify
        self.token = token
        self.email = email
        self.default_headers = {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json'
        }

    def find_user_by_email(self):
        encoded = urlencode({'email': self.email})
        response = requests.get('https://slack.com/api/users.lookupByEmail?{0}'.format(encoded),
                                headers=self.default_headers, verify=self.ssl_verify)
        return response.json()['user']['id']

    def update_status(self, status=None):
        current_emot = self.display_status_emot()
        update = {
            'user': self.find_user_by_email(),
            'profile': {
                'status_text': status if status else self.display_status(),
                'status_emoji': current_emot
            }
        }
        requests.post('https://slack.com/api/users.profile.set', data=json.dumps(update),
                                 headers=self.default_headers, verify=self.ssl_verify)

    def display_status_emot(self):
        return requests.get('https://slack.com/api/users.profile.get',
                            headers=self.default_headers, verify=self.ssl_verify).json()['profile']['status_emoji']

    def display_status(self):
        return requests.get('https://slack.com/api/users.profile.get',
                            headers=self.default_headers, verify=self.ssl_verify).json()['profile']['status_text']
