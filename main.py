
import os
import random
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)


@app.route('/')
def index():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 3. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return f'<h2>Hi {spotify.me()["display_name"]}, ' \
           f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
           f'<a href="/playlists">my playlists</a> | ' \
           f'<a href="/currently_playing">currently playing</a> | ' \
           f'<a href="/current_user">me</a> | ' \
           f'<a href="/tracks">Tracks</a> | ' \
           f'<a href="/player">Player</a> | ' \




@app.route('/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')


@app.route('/playlists')
def playlists():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_playlists()


@app.route('/currently_playing')
def currently_playing():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    if not track is None:
        return track
    return "No track currently playing."


@app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()















def get_artist(spotify, name):
    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    for item in items:
        if item['name'] == name:
            return item
    return None

def get_albums(spotify, artist):
    albums = []
    results = spotify.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    return albums


def get_tracks(spotify, album):
    tracks = []
    results = spotify.album_tracks(album['id'])
    for result in results['items']:
        tracks.append(result['uri'])
    return tracks


def get_artist_tracks(spotify, artist):
    artist_tracks = []
    albums = get_albums(spotify, artist)
    for album in albums:
        album_tracks = get_tracks(spotify, album)
        for album_track in album_tracks:
            artist_tracks.append(album_track)
    return artist_tracks


def show_artist_tracks(spotify, artist):
    albums = get_albums(spotify, artist)
    page = ""
    for album in albums:
        tracks = get_tracks(spotify, album)
        page += str(tracks)
    return page


@app.route('/tracks', methods=['GET'])
def tracks():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    artist = get_artist(spotify, 'DMX')
    # album = sp.artist_albums(artist['id'], album_type='album')
    return show_artist_tracks(spotify, artist)



@app.route('/player', methods=['GET'])
def player():
    scope = "user-read-playback-state,user-modify-playback-state"
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))
    artist_name = str(request.args.get('artist'))
    if artist_name == "None":
        return render_template("player.html")
    else:
        artist = get_artist(spotify, artist_name)
        tracks = get_artist_tracks(spotify, artist)
        # random_tracks = random.shuffle(tracks)
        res = spotify.devices()
        spotify.start_playback(uris=tracks)
        return res





if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))