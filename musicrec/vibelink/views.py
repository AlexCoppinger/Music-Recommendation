from django.shortcuts import render, redirect
from .spotify import search_playlists, search_tracks 
from .spotify import get_spotify_oauth, get_spotify_client
from .forms import CustomUserCreationForm
from .models import User

from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse

import spotipy 



def playlist_search_view(request):
    print("search_spotify_playlists called")
    query = request.GET.get('query', '')
    playlists = []
    if query:
        try:
            playlists = search_playlists(query)
        except Exception as e:
            return render(request, 'vibelink/search.html', {'error': str(e)})
    return render(request, 'vibelink/search.html', {'playlists': playlists})

def track_search_view(request):
    query = request.GET.get('query', '')
    tracks = []
    if query:
        try:
            tracks = search_tracks(query)
        except Exception as e:
            return render(request, 'vibelink/search.html', {'error': str(e)})
    return render(request, 'vibelink/search.html', {'tracks': tracks})

def home(request):
    return render(request, 'vibelink/home.html')

# Register view: 

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('vibelink:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'vibelink/register.html', {'form': form})

# Spotify login trigger and callback views:

def spotify_login(request):
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()

    next_url = request.GET.get('next')
    if next_url:
        request.session['next_url'] = next_url # Gets the URL the user was trying to access but wasn't logged in for 

    return redirect(auth_url)

def spotify_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('vibelink:home')

def spotify_callback(request):
    sp_oauth = get_spotify_oauth()
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        return render(request, "vibelink/error.html", {"message": f"Spotify authorization failed: {error}"})

    if code:
        try:
            token_info = sp_oauth.get_access_token(code, as_dict=True)
            access_token = token_info['access_token']
            refresh_token = token_info.get('refresh_token')
            sp = spotipy.Spotify(auth=access_token)
            profile = sp.current_user()

            # Get profile image if available
            profile_image_url = None
            if profile['images'] and len(profile['images']) > 0:
                profile_image_url = profile['images'][0]['url']
        except Exception as e:
            return render(request, "vibelink/error.html", {"message": f"Spotify token error: {e}"})

        spotify_id = profile['id']
        display_name = profile.get('display_name', '')
        uri = profile.get('uri', '')

        user, created = User.objects.get_or_create(
            spotify_id=spotify_id,
            defaults={
                'display_name': display_name,
                'username': spotify_id,  # Required for AbstractUser
                'uri': uri,
                'spotify_access_token': access_token,
                'spotify_refresh_token': refresh_token,
                'profile_image': profile_image_url,
            }
        )

        # If the user already existed, update tokens just in case
        if not created:
            user.profile_image = profile_image_url # in case profile image was changed 
            user.spotify_access_token = access_token
            user.spotify_refresh_token = refresh_token
            user.save()

        login(request, user)  # Log the user in using Django's login system and the user's spotify credentials

        next_url = request.session.pop('next_url', None) # Gets the next URL to redirect to that 
        if next_url:
            return redirect(next_url)
        
        return redirect('vibelink:home')
    


# Using the client

def show_profile(request):
    sp = get_spotify_client(request)
    me = sp.current_user()
    return JsonResponse(me)


# view for displaying playlist tracks
def playlist_tracks_view(request, playlist_id):
    try:
        playlist = Playlist.objects.get(spotify_id=playlist_id)
        tracks = get_playlist_tracks(playlist_id)
        return render(request, 'vibelink/playlist_tracks.html', {
            'playlist': playlist,
            'tracks': tracks
        })
    except Exception as e:
        return render(request, 'vibelink/search.html', {'error': str(e)})