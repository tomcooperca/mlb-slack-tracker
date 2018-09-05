import requests
import os

class Token():
    def __init__(self, auth_code, client_id, client_secret):
        self.auth_code = auth_code
        self.client_id = client_id
        self.client_secret = client_secret


    def generate_token(self):
        oauth_params = {
            "code": self.auth_code,
            "redirect_uri": "https://mlb-slack-tracker.herokuapp.com/authorize",
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.get('https://slack.com/oauth/authorize', params=oauth_params)
        print("Token response: {}".format(response.text))
        return response.json()
