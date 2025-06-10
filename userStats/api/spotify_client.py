import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv



load_dotenv()
# SpotifyClient class to handle Spotify API interactions
class SpotifyClient:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")                                     # Ensure these environment variables are set
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")                             # Ensure these environment variables are set              
        self.redirect_uri = os.getenv("SPOTFY_REDIRECT_URI")                                # Ensure these environment variables are set
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError("Missing Spotify API credentials in environment variables.")
        self.scope = "user-read-recently-played user-top-read"
        self.sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope
        )

    # Returns the Spotify authorization URL for user login.
    def get_auth_url(self):
        return self.sp_oauth.get_authorize_url()

    # Exchanges the authorization code for an access token.
    def get_access_token(self, code):
        try:
            # print("Getting access token with code:", code)
            token = self.sp_oauth.get_access_token(code)
            if isinstance(token, dict) and 'access_token' in token:
                # print("Access token received:", token['access_token'])
                return token
            else:
                print("Invalid token response:", token)
                return None
        except Exception as e:
            # Optionally log the error
            return Exception(f"Error getting access token: {e}")

    # Returns an authenticated Spotify client using the provided access token.
    def get_spotify_client(self, token):
        """Returns an authenticated spotipy.Spotify object."""
        return spotipy.Spotify(auth=token)

    # Example API call: get user’s top tracks
    def get_user_top_tracks(self, token, limit=10, time_range='medium_term'):
        sp = self.get_spotify_client(token)
        return sp.current_user_top_tracks(limit=limit, time_range=time_range)['items']

    # Example API call: get user’s top artists
    def get_user_top_artists(self, token, limit=10, time_range='medium_term'):
        sp = self.get_spotify_client(token)
        return sp.current_user_top_artists(limit=limit, time_range=time_range)['items']

    # Example API call: get recently played tracks
    def get_recently_played(self, token, limit=10):
        sp = self.get_spotify_client(token)
        return sp.current_user_recently_played(limit=limit)['items']

    # Example API call: get user’s playlists
    def get_user_playlists(self, token, limit=10):
        sp = self.get_spotify_client(token)
        return sp.current_user_playlists(limit=limit)['items']
    
    def get_user_profile(self, token):
        sp = self.get_spotify_client(token)
        return sp.current_user()