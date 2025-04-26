from django.urls import path
from . import views

app_name = 'vibelink'

urlpatterns = [
    path('search/', views.search_playlists, name='search_playlists'),
    path('', views.home, name='home')
]