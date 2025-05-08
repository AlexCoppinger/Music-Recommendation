import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from django.conf import settings

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                     client_id=settings.SPOTIFY_CLIENT_ID, 
                     client_secret=settings.SPOTIFY_CLIENT_SECRET
                     ))


def search_playlists(query):
    """
    Search for playlists on Spotify based on a query.

    Args:
        query (str): The search query.

    Returns:
        list: A list of playlist names matching the query.
    """
    print("search_playlists called")
    results = sp.search(q=query, type='playlist', limit=10)
    playlists = results['playlists']['items']
    return [playlist['name'] for playlist in playlists]

def search_tracks(query):

    print("search_tracks called") # For seeing
    results = sp.search(q=query, type='track', limit=10)
    print(results) # For seeing
    tracks = results['tracks']['items']
    
    if not tracks:
        print("No tracks found") # just in case this doesn't work
        return []
    

    return [track['name'] for track in tracks]


# The syntax for this is: you will be returned a variable with all the data:
# To access it you have (imagining it goes into the variable playlists) playlists[][]
# Now, you can open playlists using playlists[n]['type'] where n is the number of the playlist in the list
# and to access the list of type, you can enter playlists[n].keys()


# We want our Django app to:
# Authenticate itself with Spotify using the Client Credentials Flow
# Use the Spotify API to request public data
# Return that data via Django views or use it inside your app (on the html page)


# For this module:
# We use this spotipy to wrap the Spotify API in Python functions
# Use this module to organize the API logic
# Django views to interact with users and return data

