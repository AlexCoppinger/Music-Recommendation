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
    path('vibes/', views.vibes_view, name='vibes'),
    path('vibes/new/', views.new_vibe_view, name='new_vibe'),
    path('vibe/<str:vibe_name>/', views.vibe_detail_view, name='vibe_detail'),
    path('vibe/<int:vibe_id>/update-description/', views.update_vibe_description, name='update_vibe_description'),
    path('vibes/delete/<int:uservibe_id>/', views.delete_vibe_view, name='delete_vibe'),
    # Add a path to rate the song for the specific algorithm/user
    path('rate/song', views.rate_song_view, name='rate_song'),
    path('play-track/', views.play_track, name='play_track'),
    path('submit-rating/', views.submit_rating, name='submit_rating'),
    
]

