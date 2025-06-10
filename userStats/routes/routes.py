from flask import Blueprint, render_template, session, redirect, request, url_for

from userStats.api.spotify_client import SpotifyClient




main = Blueprint('main', __name__)

spotify = SpotifyClient()

@main.route('/')
def index():
    return render_template("login.html", auth_url=spotify.get_auth_url())


@main.route('/callback')
def callback():
    code = request.args.get('code')
    # print("Callback: code received =", code)
    if not code:
        return redirect(url_for('main.index'))  # Or return an error message
    token_info = spotify.get_access_token(code)
    # print("Callback token_info:", token_info)
    if not token_info:
        return redirect(url_for('main.index'))  # Or show an error
    session['token_info'] = token_info
    
    return redirect(url_for('main.dashboard'))
    


"""
Renders the dashboard page for the authenticated user.
This function performs the following steps:
1. Retrieves the user's token information from the session.
2. If no token is found, redirects the user to the login page.
3. Checks if the access token is expired:
    - If expired, attempts to refresh the access token using the refresh token.
    - If refreshing fails, redirects the user to the login page.
4. Retrieves the access token from the token information.
    - If not found, redirects the user to the login page.
5. Uses the access token to fetch the user's top tracks, top artists, recently played tracks, and user profile from Spotify.
    - If any API call fails, redirects the user to the login page.
6. Renders the 'dashboard.html' template, passing the fetched user data for display.
Returns:
    A rendered HTML template for the dashboard if successful, otherwise a redirect to the login page.
"""
@main.route('/dashboard')
def dashboard():
    token_info = session.get('token_info')
    if not token_info:
        return redirect(url_for('main.index'))
    if spotify.sp_oauth.is_token_expired(token_info):
        try:
            token_info = spotify.sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
        except Exception:
            return redirect(url_for('main.index'))
    token = token_info.get('access_token')
    if not token:
        return redirect(url_for('main.index'))
    try:
        top_tracks = spotify.get_user_top_tracks(token)
        top_artists = spotify.get_user_top_artists(token)
        recent_tracks = spotify.get_recently_played(token)
        user_profile = spotify.get_user_profile(token)
    except Exception:
        return redirect(url_for('main.index'))
    return render_template(
        'dashboard.html',
        top_tracks=top_tracks,
        top_artists=top_artists,
        recent_tracks=recent_tracks,
        user_profile=user_profile
    )