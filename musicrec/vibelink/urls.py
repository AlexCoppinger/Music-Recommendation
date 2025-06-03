from django.urls import path
from . import views

app_name = 'vibelink'

urlpatterns = [
    path('search/', views.playlist_search_view, name='search_playlists'),
    path('search/tracks/', views.track_search_view, name='search_tracks'),  # Updated path
    path('', views.home, name='home'),
    # Stuff for authentication:
    path('spotify/login/', views.spotify_login, name='login'),
    path('spotify/logout/', views.spotify_logout, name='logout'),
    path('spotify/callback/', views.spotify_callback, name='callback'),
    #path('playlist/<str:playlist_id>/tracks/', views.playlist_tracks_view, name='playlist_tracks'),

    # Add a path to see the set of algorithms for the user
    path('algorithms/', views.algorithms_view, name='algorithms'),
    # Add a path to rate the song for the specific algorithm/user
    path('rate/song', views.rate_song_view, name='rate_song'),
]

