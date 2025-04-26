from django.shortcuts import render
from .spotify import search_playlists

def search_playlists(request):
    print("search_spotify_playlists called")
    query = request.GET.get('query', '')  # Get the search query from the request
    playlists = []  # Default empty list for playlists
    if query:  # If a query is provided
        try:
            playlists = search_playlists(query)  # Call the Spotify API function
        except Exception as e:
            return render(request, 'vibelink/search.html', {'error': str(e)})
    return render(request, 'vibelink/search.html', {'playlists': playlists})

def home(request):
    return render(request, 'vibelink/home.html')