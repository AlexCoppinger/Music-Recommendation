from django.db import models


class User(models.Model):
    display_name = models.CharField(max_length=255, blank=True, default='', null=True)

class Track(models.Model):
    """
    Model representing a track in a Spotify playlist.
    """
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, null=True, blank=True)
    album = models.CharField(max_length=255)
    duration_ms = models.IntegerField(null=True)  # Add this
    uri = models.CharField(max_length=255, null=True, blank=True)
    preview_url = models.URLField(null=True, blank=True)
    playlist_name = models.CharField(max_length=255, blank=True, default='', null=True)  # Name of the playlist the track belongs to

    def __str__(self):
        return f"{self.name} by {self.artist}"
    
    
class Playlist(models.Model):
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    track_count = models.IntegerField()

    def __str__(self):
        return self.name