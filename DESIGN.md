# JUSTify - Design
One day I was teaching a jiu jitsu class and reeeaally wanted to play only music
by DMX and IDLES, but that would be such a hassle to make a queue or a playlist for 
such a silly thing like playing music for a martial arts class.

Thus the idea was birthed!  How cool would it be if I had an app that could do that
menial/ tedious task for me?

This app (titled JUSTify- as in JUST the artists you want to listen to) connects to
Spotify's web API (https://developer.spotify.com/) via a python library called Spotipy 
(https://spotipy.readthedocs.io/en/2.21.0/), and allows a user to sign in or register 
for a Spotify account, and once signed in, the user can then select up to 4 artists
(currently the artists must be perfectly spelled- capitalization and symbols included)
and the APP will make calls to the API and create a shuffled queue of the top 10 songs
from each artist's discography on the user's device, that is 
connected to Spotify (and selected at the prompt), that will automatically play on the
selected device.


## Steps:

## Spotify Developer Keys
First step I took was to get developer keys and add them as environment variables.

- First I created a developer account by logging into Spotify for Developers via my
Spotify account.
- Next I "created an APP" to gain access to my CLIENT_ID and CLIENT_SECRET.
- Then I added a flask redirect URI to the "Redirect URI" form on my developer account.
- Then I added all of these settings to my environment variables in my PyCharm IDE  
(as well as a PORT number) and started coding.

## Spotipy Package, Python, and Flask
This project was written entirely in python using PyCharm while utilizing
Flask.

I also used Spotipy allows users to have access to all of the music data in Spotify's platform by
binding python to Spotify's web API.

The main tools I used from this package were:
- "cache_handler" used in my index function to save authorization tokens during this session.
- "SpotifyOAuth" to gain access to protected data
- The past two specifically helped me log in to spotify as a user to gain access to the API
to manipulate data from.
- To get access to an artist I created a function get_artist that uses the "search" function from
spotipy.  With this I can create artist search queries.  The info you get from spotify is in
the form of very large JSON files, so here I had to be very specific with where I get my info
from (eg. results = ['artists']['items'])
- The most important function I created is

controls external spotify audio app that is connected to your device. This is intentional because

what tools I used
mimiced log in/ log out from spotipy example

## CSS
Python/ flask
- list of functions

file based flask session to store log in sessions

css

## Backlog for future development
- mm
- 