from django.shortcuts import render
from .spotify import search_playlists as spotify_search_playlists, search_tracks as spotify_search_tracks

def playlist_search_view(request):
    print("search_spotify_playlists called")
    query = request.GET.get('query', '')
    playlists = []
    if query:
        try:
            playlists = spotify_search_playlists(query)
        except Exception as e:
            return render(request, 'vibelink/search.html', {'error': str(e)})
    return render(request, 'vibelink/search.html', {'playlists': playlists})

def track_search_view(request):
    query = request.GET.get('query', '')
    tracks = []
    if query:
        try:
            tracks = spotify_search_tracks(query)
        except Exception as e:
            return render(request, 'vibelink/search.html', {'error': str(e)})
    return render(request, 'vibelink/search.html', {'tracks': tracks})

def home(request):
    return render(request, 'vibelink/home.html')