import requests
import os

class Token():
    def __init__(self, auth_code, redirect_uri, client_id, client_secret):
        self.auth_code = auth_code
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret


    def generate_token(self):
        oauth_params = {
            "code": self.auth_code,
            "redirect_uri": self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.get('https://slack.com/api/oauth.access', params=oauth_params)
        if (response.status_code == 200):
            return response.json()
        return None
