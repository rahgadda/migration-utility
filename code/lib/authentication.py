from authlib.integrations.requests_client import OAuth2Session
import os
import requests

# Loading Google OAuth2 credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
AUTHORIZE_URL = os.getenv('AUTHORIZE_URL')
TOKEN_URL = os.getenv('TOKEN_URL')

class GoogleAuthenticator:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.redirect_uri = REDIRECT_URI
        self.authorize_url = AUTHORIZE_URL
        self.token_url = TOKEN_URL
        self.oauth = OAuth2Session(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope='openid email profile',
        )

    def get_authorization_url(self):
        return self.oauth.create_authorization_url(self.authorize_url)

    def fetch_token(self, code):
        token = self.oauth.fetch_access_token(self.token_url, authorization_response=code)
        return token
        