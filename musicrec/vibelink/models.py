from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    display_name = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=255)  # Unique identifier for the user in Spotify
    profile_image = models.URLField(blank=True, null=True)  # URL to the user's profile image in Spotify
    uri = models.CharField(max_length=255, blank=True, null=True)  # URI for the user in Spotify
    spotify_access_token = models.CharField(max_length=255, blank=True, null=True)
    spotify_refresh_token = models.CharField(max_length=255, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

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
    

# this model represents the link between tracks and playlists
class TrackPlaylist(models.Model):
    """
    Model representing the many-to-many relationship between tracks and playlists.
    """
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('track', 'playlist')

    def __str__(self):
        return f"{self.track.name} in {self.playlist.name}"