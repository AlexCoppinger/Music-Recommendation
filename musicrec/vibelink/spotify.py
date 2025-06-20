import spotipy
from spotipy.cache_handler import MemoryCacheHandler

from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import User, TrackSearchResult, PlaylistSearchResult
from django.conf import settings
from .models import Track, Playlist, User, TrackPlaylist, Vibe



import datetime

## This is the code for the Spotify API integration but it will probably get 
## moved to the functions below in the future
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                     client_id=settings.SPOTIFY_CLIENT_ID, 
                     client_secret=settings.SPOTIFY_CLIENT_SECRET
                     ))



# This section is for searching for playlists and tracks
# and saving them to the database

def import_items(query, type, force_new=False, limit=50):
    """
    Import items from Spotify based on the query and type.
    """
    # Get a Spotify client
    sp = get_spotify_client()

    # Initialize our context
    context = {
        'playlists': [],
        'tracks': [],
        'query': query,
        'type': type,
        'force_new': force_new,
        'using_existing_search_results': not force_new,
    }

    # Check whether we've imported items for this search query
    done = False
    total_imported = 0  # Track the total number of items imported
    is_first = True

    while not done:
        if is_first:
            # Search for the first batch of results
            results = sp.search(q=query, type=type, limit=limit)
            is_first = False
        else:
            # Search for the next batch of results
            results = sp.next(curr_results)

        curr_results = results[f"{type}s"]

        # Extract the items from the results
        items = curr_results['items']
        if not items:
            done = True
            break

        for item in items:
            if not item:
                print("Skipping invalid item: None")
                continue

            # Ensure that the item has an owner field
            owner = item.get('owner')
            if not owner:
                print(f"Skipping item without owner: {item.get('name', 'Unknown')}")
                continue

            owner_name = owner.get('display_name', 'Unknown')
            print(f"Importing playlist: {item['name']} by {owner_name}")
            
            if total_imported >= limit:
                done = True
                break

            if type == 'playlist':
                p, _ = Playlist.objects.update_or_create(
                    spotify_id=item['id'],
                    defaults={
                        'name': item['name'],
                        'description': item.get('description', ''),
                        'image_url': item['images'][0]['url'] if item['images'] else '',
                    }
                )

                # Import our playlist tracks
                txp = import_playlist_tracks(p)

                # Update our track list
                context['tracks'].extend([t.track.id for t in txp])

                # Add the playlist to our context
                context['playlists'].append(p.id)
                total_imported += 1

            elif type == 'track':
                t, _ = Track.objects.update_or_create(
                    spotify_id=item['id'],
                    defaults={
                        'name': item['name'],
                        'uri': item['uri'],
                        'artist': item['artists'][0]['name'],
                        'album': item['album']['name'],
                        'duration_ms': item['duration_ms'],
                        'preview_url': item['preview_url'],
                        'image_url': item['album']['images'][0]['url'] if item['album']['images'] else '',
                    }
                )
                context['tracks'].append(t.id)
                total_imported += 1

        # Check if there are more results
        if not curr_results['next']:
            done = True

    # Convert the context lists to QuerySets
    context['playlists'] = Playlist.objects.filter(id__in=context['playlists'])
    context['tracks'] = Track.objects.filter(id__in=context['tracks'])

    return context

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
        show_dialog=True,  # Do not show the dialog for user consent
        cache_handler=MemoryCacheHandler(),  # Disable caching to avoid issues with session management
    )

def get_spotify_client_credentials():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_spotify_client(request=None):
    if request and 'token_info' in request.session:
        token_info = request.session['token_info']
        now = int(datetime.datetime.now().timestamp())
        is_expired = token_info.get('expires_at', 0) - now < 60

        if is_expired:
            sp_oauth = get_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            request.session['token_info'] = token_info

        return spotipy.Spotify(auth=token_info['access_token'])

    return get_spotify_client_credentials()
    
# Done with user authentication and login


# Method to fecth tracks from a playlist
def import_playlist_tracks(playlist):
    """
    Import tracks from a Spotify playlist into the database.
    
    Args:
        playlist (dict): The playlist data from Spotify API.
    """
    # Get the Spotify client
    sp = get_spotify_client()
    
    done = False
    result = None

    while not done:
        if not result:
            # Get the first tracks from the playlist
            result = sp.playlist_tracks(playlist.spotify_id)    
        else:
            # Get the next tracks from the playlist
            result = sp.next(result)
        
        track_num = 0
        # Iterate through the tracks and import them
        for item in result['items']:
            track = item['track']

            if not track:
                continue
            
            # Create or update the track in the database
            t, _ = Track.objects.update_or_create(
                spotify_id=track['id'],
                defaults={
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'duration_ms': track['duration_ms'],
                    'preview_url': track.get('preview_url'),
                    'uri': track.get('uri'),
                    'image_url': track['album']['images'][0]['url'] if track['album']['images'] else ''
                }
            )

            # Increment the track number
            track_num += 1

            # Create our TrackXPlaylist object
            TrackPlaylist.objects.update_or_create(
                track=t,
                playlist=playlist,
                defaults={
                    'order': track_num,
                }
            )

        # Check if there are more tracks to fetch
        if result['next']:
            done = False
        else:
            done = True

    # Return the Playlist tracks
    return TrackPlaylist.objects.filter(playlist=playlist).order_by('order')


def create_vibe(user, vibe_name, description):
    """
    Create a new vibe for the user.
    """
    if not user:
        raise ValueError("User must be provided")

    vibe = Vibe.objects.create(
        user=user,
        name=vibe_name,
        description=description
    )
    return vibe

