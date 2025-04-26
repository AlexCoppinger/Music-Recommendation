from django.urls import path
from .views import search_spotify_playlists

app_name = 'vibelink'

urlpatterns = [
    path('', search_spotify_playlists, name='search_playlists')
]