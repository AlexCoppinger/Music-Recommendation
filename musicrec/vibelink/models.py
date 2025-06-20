from django.db import models
from django.contrib.auth.models import AbstractUser
from importlib import import_module



class User(AbstractUser):
    display_name = models.CharField(max_length=255)
    spotify_id = models.CharField(max_length=255, unique=True)  # Unique identifier for the user in Spotify
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
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True, default='', null=True)
    album = models.CharField(max_length=255)
    duration_ms = models.IntegerField()
    spotify_id = models.CharField(max_length=255, unique=True, null=True)  # Unique identifier for the track in Spotify
    uri = models.CharField(max_length=255, blank=True, null=True)  # URI for the track in Spotify
    preview_url = models.URLField(blank=True, null=True)  # URL for the track preview
    image_url = models.URLField(blank=True, null=True)  # URL for the track's album art
    
    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'
        ordering = ['name']
    # Add any additional fields or methods as needed
    
    
class Playlist(models.Model):
    """
    Model representing a Spotify playlist.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    spotify_id = models.CharField(max_length=255, unique=True)  # Unique identifier for the playlist in Spotify
    uri = models.CharField(max_length=255, blank=True, null=True)  # URI for the playlist in Spotify

    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
        ordering = ['name']
    

# his model represents the link between tracks and playlists
class TrackPlaylist(models.Model):
    """
    Model representing the many-to-many relationship between tracks and playlists.
    """
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='tracks')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    order = models.IntegerField(default=0)  # To maintain the order of tracks in the playlist

    class Meta:
        unique_together = ('track', 'playlist')

    def __str__(self):
        return f"{self.track.name} in {self.playlist.name}"
    
class Vibe(models.Model):
    """
    Model representing a recommendation algorithm.
    """
    name = models.CharField(max_length=255)
    # Can't be blank apparently, so I'm adding a blank default
    description = models.TextField(blank=True, default='')  # Description of the algorithm
    # The algorithm used for recommendations (e.g., collaborative filtering, content-based)
    algorithm_type = models.CharField(max_length=255, blank=True)

    callback = models.CharField(max_length=255, blank=True)  # Callback function for the algorithm

    def execute_callback(self, **kwargs):
        """
        Execute the callback function for the algorithm.
        This function basically recieves a bunch of arguments for its creation 
        and when executed can call the function specified in the callback field.
        It imports the module and calls the method specified in the callback field.

        """
    # Check whether we specified by a module and a method
        modules = self.callback.split('.')

        # The actual method is at the end
        method = modules.pop()

        module = import_module('.'.join(modules))

        function = getattr(module, method)

        result = function(self, **kwargs)

        return result

        # Call the callback function with the request and optional parameters
    
class UserVibe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_vibes')
    vibe = models.ForeignKey(Vibe, on_delete=models.CASCADE, related_name='vibe_users')
    search_term = models.CharField(max_length=255)  # This is the "vibe" search query

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'vibe')  # Prevent duplicates

    def __str__(self):
        return f"{self.user.username} - {self.vibe.name} ({self.search_term})"
    

# Create a UserVibePlaylist model if you need to store additional information about the relationship
class UserVibePlaylist(models.Model):
    """
    Model representing the many-to-many relationship between UserVibe and Playlists.
    This preserves the context of which search term caused which playlists to be saved.
    """
    # This will keep Users and vibes together with the playlists so that we can track everything together when loading playlists
    user_vibe = models.ForeignKey(UserVibe, on_delete=models.CASCADE, related_name='UserVibes_playlists', null=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_vibe', 'playlist')

    def __str__(self):
        return f"{self.user_vibe.user.username} - {self.user_vibe.vibe.name} - {self.playlist.name}"



class UserXTrack(models.Model):
    """
    Model representing the many-to-many relationships between users and tracks.
    """
    user = models.ForeignKey(User, related_name='user_tracks', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, related_name='track_users', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'track')  # Ensure a user can only have one instance of a track

    def __str__(self):
        return f"{self.user.name} - {self.track.name}"

class TrackRating(models.Model):
    RATING_CHOICES = [
        (1, 'Strongly Agree'),
        (2, 'Somewhat Agree'),
        (3, 'Neither Agree nor Disagree'),
        (4, 'Somewhat Disagree'),
        (5, 'Strongly Disagree'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vibe = models.ForeignKey(Vibe, on_delete=models.CASCADE, null=True, blank=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')

    def update_coefficient(self, vibe_name):
        """
        Update the coefficient value for the track.
        """
        callback = Vibe.objects.get(name=vibe_name).callback

        # Call the callback function to update the coefficient
 


class PlaylistSearchResult(models.Model):
    """
    Model to associate a search query with imported playlists.
    """
    query = models.CharField(max_length=255)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    imported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('query', 'playlist')  # Ensure uniqueness of query and playlist

    def __str__(self):
        return f"Query: {self.query} - Playlist: {self.playlist.name}"


class TrackSearchResult(models.Model):
    """
    Model to associate a search query with imported tracks.
    """
    query = models.CharField(max_length=255)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    imported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('query', 'track')  # Ensure uniqueness of query and track

    def __str__(self):
        return f"Query: {self.query} - Track: {self.track.name}"

class TrackCoefficient(models.Model):
    """
    Model to store track coefficients based on user ratings.
    This is actually where most of the computations may happen. 
    When we get a search term from UserVibe, the search term will search 
    for a playlist, then we run the computations on all the playlists
    and put all the tracks (including their coefficients) into this. 
    We can then backtrack using the playlists that were saved to run the calculations
    """
    track = models.ForeignKey('Track', on_delete=models.CASCADE)
    vibe = models.ForeignKey('Vibe', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    coefficient = models.FloatField(default=0.0)  # Coefficient value for the track
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('track', 'vibe', 'user')
        ordering = ['-coefficient']
        # Order by coefficient in descending order

class PlaylistSearchResult(models.Model):
    """
    Model to associate a search query with imported playlists.
    """
    query = models.CharField(max_length=255)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    imported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('query', 'playlist')  # Ensure uniqueness of query and playlist

    def __str__(self):
        return f"Query: {self.query} - Playlist: {self.playlist.name}"


class TrackSearchResult(models.Model):
    """
    Model to associate a search query with imported tracks.
    """
    query = models.CharField(max_length=255)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    imported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('query', 'track')  # Ensure uniqueness of query and track

    def __str__(self):
        return f"Query: {self.query} - Track: {self.track.name}"

