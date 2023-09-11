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

        