from django.contrib import admin
from django.apps import apps

# Use lazy loading to get the models
Playlist = apps.get_model('vibelink', 'Playlist')
Track = apps.get_model('vibelink', 'Track')

admin.site.register(Playlist)
admin.site.register(Track)