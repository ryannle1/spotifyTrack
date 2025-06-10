from flask import Flask
from userStats._init_ import create_app
from flask import session, redirect, request, url_for, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from userStats.routes.routes import main

app = create_app()
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)