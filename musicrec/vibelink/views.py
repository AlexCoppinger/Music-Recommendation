from django.shortcuts import render, redirect
from .spotify import search_playlists, search_tracks 
from .spotify import get_spotify_oauth, get_spotify_client
from .forms import CustomUserCreationForm

from django.contrib.auth import login
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

# To try to login

def spotify_login(request):
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.redirect_uri
    return redirect(auth_url)

# callback view


def spotify_callback(request):

    print("made it to spotify_callback")

    sp_oauth = get_spotify_oauth()
    session = request.session

    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        return render(request, "error.html", {"message": f"Spotify authorization failed: {error}"})

    if code:
        try:
            token_info = sp_oauth.get_access_token(code, as_dict=True)
        except Exception as e:
            return render(request, "error.html", {"message": f"Failed to get access token: {str(e)}"})

        session['token_info'] = token_info  # You can save to DB if you want
        # WILL SAVE IT SOON

        # Give this a try: 
        

        return redirect('vibelink:home')  # Or wherever your app continues
    else:
        return render(request, "error.html", {"message": "No authorization code provided"})
    


# Using the client

def show_profile(request):
    sp = get_spotify_client(request)
    me = sp.current_user()
    return JsonResponse(me)