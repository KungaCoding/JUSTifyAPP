from flask import Flask
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials, SpotifyOAuth
import argparse
# from routes import urls_blueprint

app = Flask(__name__)

def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None

def get_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    return albums


def get_tracks(album):
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def show_artist_tracks(artist):
    albums = get_albums(artist)
    page = ""
    for album in albums:
        tracks = get_tracks(album)
        page += str(tracks)
    return page


@app.route('/', methods=['GET'])
def index():
    artist = get_artist('DMX')
    # album = sp.artist_albums(artist['id'], album_type='album')
    return show_artist_tracks(artist)

if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    # main()
    app.run(port=5001)


