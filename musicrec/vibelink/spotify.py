import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from django.conf import settings
from .models import Track
from .models import Playlist


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                     client_id=settings.SPOTIFY_CLIENT_ID, 
                     client_secret=settings.SPOTIFY_CLIENT_SECRET
                     ))


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

