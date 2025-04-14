from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_spotify_playlists, name='search_playlists')
]