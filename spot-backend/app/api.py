from flask import Flask, Blueprint, jsonify, request, redirect, session, url_for, abort
import os
from dotenv import load_dotenv
from .spotify import get_auth_url, get_access_token

load_dotenv()


CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'http://accounts.spotify.com/api/token'


def configure_routes(app):
    @app.route("/")
    def home():
        return '<a href="login>Login with Spotify</a>'
    
    @app.route("/login")
    def login():
        return redirect(get_auth_url)
    
    @app.route("/callback")
    def callback():
        code = request.args.get('code')
        error = request.args.get('error')
        session_state = session.pop('oauth_state',None)
        request_state = request.args.get('state')


        if error:
            print(f"Error: {error}")
            abort(403)
        if not session_state or not request_state or session_state != request_state:
            print("Session state and request state do not match or state error.")
            abort(403)

        token_info = get_access_token(code)
        return token_info
