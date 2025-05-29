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
]