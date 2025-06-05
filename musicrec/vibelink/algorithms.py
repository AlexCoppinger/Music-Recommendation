from vibelink.models import Vibe, TrackCoefficient, Track, TrackRating, PlaylistSearchResult, TrackXPlaylist
from django.db.models import Count

def update_track_weights(request, **kwargs):
    """
    Update the track weights in the TrackCoefficient model.
    """
    # Get the algorithm name from the request
    algorithm_name = request.session.get('algorithm_name', None)

    # Get the algorithm object
    if not algorithm_name:
        # Don't touch the weights
        algorithm_name = 'popular_relation'
    
    algorithm = Vibe.objects.get(name=algorithm_name)

    # Use the algorithm's callback function to update the coefficient
    success = algorithm.execute_callback(**kwargs)

    return success


# Define our popular relation function
def popular_relation(algorithm, **kwargs):
    """
    Update the track weights based on the popular relation algorithm.
    """
    trackrating = kwargs.get('track_rating', None)
    if not trackrating:
        return False
    
    # Get the track from the trackrating
    track = trackrating.track

    # Get the selected purpose from the request
    purpose = trackrating.purpose

    # Fetch the tracks for the playlists that match the query
    playlists = TrackXPlaylist.objects.filter(track=track, playlist__playlistsearchresult__query=purpose.name).values_list('playlist', flat=True).distinct()

    # Get the playlists that match the query
    txp = TrackXPlaylist.objects.filter(playlist__in=playlists)

    # Tally up the number of times a track appears across the playlists
    # Determine the most commonly used tracks
    annotated_tracks = txp.values('track').annotate(count=Count('track'))

    # Define a scaling factor lambda that implements a sigmoid function
    scaling_factor = lambda x: 1 / (1 + (1 / (1 + x))) - 0.5

    # Extract the maximum value from the rating choices
    max_value = max([choice[0] for choice in TrackRating.RATING_CHOICES])

    # Get the mean choice value
    mean_choice_value = sum([choice[0] for choice in TrackRating.RATING_CHOICES]) / len(TrackRating.RATING_CHOICES)

    # Apply the liking rating
    like_scaling = max_value - trackrating.like_rating + 1 - mean_choice_value

    # Loop over tracks and update the weights
    for track in annotated_tracks:
        # Get the track coefficient object
        track_coefficient, created = TrackCoefficient.objects.get_or_create(track=Track.objects.get(pk=track['track']), user=trackrating.user, algorithm=algorithm)

        # Update the coefficient value based on the rating
        track_coefficient.coefficient += scaling_factor(track['count']) * like_scaling

        # Save the updated coefficient value
        track_coefficient.save()

    return True