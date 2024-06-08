import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlencode
import secrets
import string
from flask import session

#Load environment variables
load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'http://accounts.spotify.com/api/token'

def get_auth_url():
    state = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
    session['oauth_state'] = state  # Store the state in the user's session
    params = {
        'client_id' : CLIENT_ID,
        'redirect_uri' : REDIRECT_URI,
        'response_type: ' : 'code',
        'scope' : 'user-read-private user-read-email',
        'state' : state
        
    }
    url = f"{AUTH_URL}?{urlencode(params)}"
    return url
    
def get_access_token(code):
    params = {
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET,
        'code' : code,
        'grant_type' : 'authorization_code',
        'redirect_uri' : REDIRECT_URI,
    }
    response = requests.post(TOKEN_URL,data=params)
    return response.json()
