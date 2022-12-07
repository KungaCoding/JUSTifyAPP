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

The main tools I used from this package and important functions created with it  were:
- "cache_handler" used in my index function to save authorization tokens during this session.
- "SpotifyOAuth" to gain access to protected data
- The past two specifically helped me log in to spotify as a user to gain access to the API
to manipulate data from (i mimicked what was written for logging in from the examples spotipy shows on their github 
directory)
- To get access to an artist I created a function get_artist that uses the "search" function from
spotipy.  With this I can create artist search queries.  The info you get from spotify is in
the form of very large JSON files, so here I had to be very specific with where I get my info
from (eg. results = ['artists']['items'])
- The most important function I created is "player()":
  - Player is designed to have buttons for playing, pausing, going to the previous or next track, as well as a form to 
  input artists, and to create the query for songs themselves.  A lot is going on here so I will summarize. 
  - Because this is still a work in process, i made the player buttons act also as refresh buttons.  This helps in 
  changing the state of the pause/ play button while also updating the visual of which song is shown (later to be 
  implemented as a javascript alert).
  - When the play button or the create play list button from the query form is selected,"spotify.start_playback()" is 
  used which will play the music connected to the device i am connected to (more on that later)
  - From the form, users input artist names.  Using request.args.get I retrieve that info and run the "get_artist" 
  function I made.  This function I use spotipy search with the query 
  (q='artist:' + name, type='artist')['artist']['items'] and iterate over it for every item in the list if the name
  of the artist is equivalent to the name it was given, the "item", which refers to the artists ID number, is returned.
  - After getting the artist, i run a function I created titled get_artist_tracks which populates a list that contains
  uri's by using spotipy's artist_top_tracks(artist['uri']).  This allows me to gain uri's for top 10 songs from every
  selected artist.
  - next, I make a list for every list of top 10 tracks, shuffle the list with random.shuffle and by using the devices 
  function from spotify (which shows a list as well as connects to all current devices connected to my account)
  - The playback controls external spotify audio app that is connected to my device. This is intentional because I 
  wanted to be able to use this app with the highest audio quality possible, there may be a loss in quality by using
  an embedded spotify player


## CSS
Not a whole lot of special things going on in my CSS.  I just wanted the colorization to match spotify as best as I could
and also have a sign out navigation button at the top that changes color when hovered on.

## Backlog for future development
- Fuzzy search for artists with complex names so I can have better ease finding artists i want to listen to.
- I'd like my buttons to not refresh the page.
- Instead of the page refreshing and using jinja to show what song is playing, I would like to have a javascript
alert pop up every time a new song is played.
- It would be really cool to be able to listen to more than just the top 10 songs.  Should be an easy implementation