from flask import Flask
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials, SpotifyOAuth
import argparse
# from routes import urls_blueprint

app = Flask(__name__)

# app.register_blueprint(urls_blueprint)

# SPOTIPY_CLIENT_ID = '68e71e0a3b2344d4942c2449a217a59e'
# SPOTIPY_CLIENT_SECRET = '8150ee0dfe834c079ad6b7ab9d8bbe61'
# #
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
#                                                client_secret=SPOTIPY_CLIENT_SECRET,
#                                                redirect_uri='https://kasperowski.com/',
#                                                scope="user-library-read"))


def get_args():
    parser = argparse.ArgumentParser(description='Shows albums and tracks for given artist')
    parser.add_argument('-a', '--artist', required=True,
                        help='Name of Artist')
    return parser.parse_args()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_album_tracks(album):
    tracks = []
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for i, track in enumerate(tracks):
        print('%s. %s', i+1, track['name'])
    return track['name']



def show_artist(artist):
    page = """"===={}====""".format(artist['name'])
    page += """Popularity: {}""".format(artist['popularity'])
    if len(artist['genres']) > 0:
        page += """Genres: {}""".format(','.join(artist['genres']))
    return page


def main():
    # args = get_args()
    # artist = get_artist(args.artist)

    # artist_input = input("Search for an Artist: ")
    artist = get_artist('DMX')
    show_artist(artist)



def get_albums(artist):
    albums = []
    results = sp.artist_albums(artist['id'], album_type='album')
    albums.extend(results['items'])
    return albums


def get_tracks(album):
    tracks = []
    track_listing = ""
    results = sp.album_tracks(album['id'])
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for track in tracks:
        track_listing += ", " + track['name']
    return track_listing


def show_artist_tracks(artist):
    albums = get_albums(artist)
    page = ""
    for album in albums:
        tracks = get_tracks(album)
        page += tracks
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



# auth_manager = SpotifyClientCredentials()
#
# scope = "user-read-playback-state,user-modify-playback-state"
# sp = spotipy.Spotify(auth_manager=auth_manager)
#
#
# # Change track
# uris=['spotify:track:6gdLoMygLsgktydTQ71b15']


