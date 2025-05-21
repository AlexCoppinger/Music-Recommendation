from django.urls import path
from . import views

app_name = 'vibelink'

urlpatterns = [
    path('search/', views.playlist_search_view, name='search_playlists'),
    path('search/tracks/', views.track_search_view, name='search_tracks'),  # Updated path
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login')
]
