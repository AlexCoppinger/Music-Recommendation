from django.db import models

class User(models.Model):
    display_name = models.CharField(max_length=255, blank=True, default='', null=True)

class Track(models.Model):
    """
    Model representing a track in a Spotify playlist.
    """
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True, default='', null=True)
    album = models.CharField(max_length=255)
    duration_ms = models.IntegerField()
    spotify_id = models.CharField(max_length=255, unique=True, null=True)  # Unique identifier for the track in Spotify
    uri = models.CharField(max_length=255, blank=True, null=True)  # URI for the track in Spotify
    preview_url = models.URLField(blank=True, null=True)  # URL for the track preview

    def __str__(self):
        return f"{self.name} by {self.artist}"
    
    
