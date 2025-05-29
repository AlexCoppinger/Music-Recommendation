import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import User
from django.conf import settings
from .models import Track
from .models import Playlist

import datetime

## This is the code for the Spotify API integration but it will probably get 
## moved to the functions below in the future
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                     client_id=settings.SPOTIFY_CLIENT_ID, 
                     client_secret=settings.SPOTIFY_CLIENT_SECRET
                     ))
## I'll have to figure out how to get the auth manager to work with this


# def get_spotify_oauth():
#     """
#     Get a Spotify OAuth object for user authentication.
#     This is used for user-specific actions like modifying playlists.
#     """
#     return SpotifyOAuth(
#         client_id=settings.SPOTIFY_CLIENT_ID,
#         client_secret=settings.SPOTIFY_CLIENT_SECRET,
#         redirect_uri=settings.SPOTIFY_REDIRECT_URI,
#         scope=settings.SPOTIFY_SCOPE,
#     )


# def get_spotify_client_credentials():
#     """
#     Get a Spotify client using client credentials flow (no user authentication).
#     Useful for general Spotify API queries that don't require user-specific data.
#     """
#     client_credentials_manager = SpotifyClientCredentials(
#         client_id=settings.SPOTIFY_CLIENT_ID,
#         client_secret=settings.SPOTIFY_CLIENT_SECRET
#     )
#     return spotipy.Spotify(client_credentials_manager=client_credentials_manager)




# This section is for searching for playlists and tracks
# and saving them to the database

def search_playlists(query, limit=25):
    offset = 0
    saved_playlists = []

    while len(saved_playlists) < limit:
        try:
            print(f"\nFetching playlists with offset {offset}...")
            results = sp.search(
                q=query,
                type='playlist',
                limit=min(50, limit - len(saved_playlists)),
                offset=offset
            )

            # Debug the raw structure
            print(f"Raw result keys: {results.keys()}")
            print(f"Playlists key: {results.get('playlists')}")
            if not results.get('playlists'):
                print("No 'playlists' key or it's None!")
                break

            playlists = results['playlists'].get('items', [])
            if not playlists:
                print("No playlist items found.")
                break

            for p in playlists:
                if p is None:
                    continue
                
                try:
                    owner_info = p.get('owner') or {}
                    tracks_info = p.get('tracks') or {}

                    playlist_data = {
                        'spotify_id': p.get('id', 'Unknown'),
                        'name': p.get('name', 'Unknown'),
                        'owner': owner_info.get('display_name', 'Unknown'),
                        'track_count': tracks_info.get('total', 0),
                    }

                    obj, created = Playlist.objects.get_or_create(
                        spotify_id=playlist_data['spotify_id'],
                        defaults=playlist_data
                    )
                    print(f"Saving playlist: {playlist_data['name']} - Created: {created}")
                    saved_playlists.append(obj)

                except Exception as e:
                    print(f"Error saving playlist {p.get('name', 'Unknown')}: {str(e)}")

            offset += len(playlists)

        except Exception as e:
            print(f"Error fetching playlists: {str(e)}")
            break

    return saved_playlists

def search_tracks(query, limit=25):
    offset = 0
    saved_tracks = []

    while len(saved_tracks) < limit:
        try:
            results = sp.search(q=query, type='track', limit=min(50, limit - len(saved_tracks)), offset=offset)
            tracks = results['tracks']['items']

            if not tracks:
                break  # No more tracks to fetch

            for track in tracks:
                try:
                    # Safely handle missing fields
                    track_data = {
                        'spotify_id': track.get('id', 'Unknown'),
                        'name': track.get('name', 'Unknown'),
                        'artist': track['artists'][0]['name'] if track.get('artists') and len(track['artists']) > 0 else 'Unknown',
                        'album': track['album']['name'] if track.get('album') else 'Unknown',
                        'duration_ms': track.get('duration_ms', 0),
                        'uri': track.get('uri', 'Unknown'),
                        'preview_url': track.get('preview_url', None),
                    }
                    obj, created = Track.objects.get_or_create(
                        spotify_id=track_data['spotify_id'],
                        defaults=track_data
                    )
                    saved_tracks.append(obj)
                    print(f"Saving track: {track_data['name']} - Created: {created}")
                except Exception as e:
                    print(f"Error saving track {track.get('name', 'Unknown')}: {str(e)}")

            offset += len(tracks)
        except Exception as e:
            print(f"Error fetching tracks: {str(e)}")
            break

    return saved_tracks





# This section will be to login and authenticate the user
# I want to authenticate a user through spotify, then create a user in the database that will have their associated
# algorithm and their spotify id
# in the future we could use their spotify id to access their playlists and tracks and play a song from their spotify app 

def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=settings.SPOTIFY_SCOPE,
    )

def get_spotify_client_credentials():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_spotify_client(request=None):
    if request and 'spotify_token_info' in request.session:
        token_info = request.session['spotify_token_info']
        now = int(datetime.datetime.now().timestamp())
        is_expired = token_info.get('expires_at', 0) - now < 60

        if is_expired:
            sp_oauth = get_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            request.session['spotify_token_info'] = token_info

        return spotipy.Spotify(auth=token_info['access_token'])

    return get_spotify_client_credentials()
    
# Done with user authentication and login


