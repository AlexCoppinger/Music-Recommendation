from vibelink.models import Vibe, TrackCoefficient, Track, TrackRating, PlaylistSearchResult, TrackPlaylist, UserVibePlaylist, UserVibe
from django.db.models import Count


# This is just to make sure that we use the proper algorithm. However, in the future, other algorithms may end up getting used
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


def popular_relation(**kwargs):
    """
    Update the track weights based on the popular relation algorithm.
    """

    trackrating = kwargs.get('track_rating', None)
    if not trackrating:
        print("No trackrating provided.")
        return False
    
    print("popular_relation: called with track:", trackrating.track.name, "by user:", trackrating.user.username)
    print("popular_relation rating:", trackrating.rating)
    user = trackrating.user
    track = trackrating.track

    # Get all vibes the user is participating in
    user_vibes = UserVibe.objects.filter(user=user)

    print(f"Found {user_vibes.count()} UserVibe(s) for user {user.username}")

    if not user_vibes.exists():
        print("No user vibes found.")
        return False

    # Get playlists associated with those vibes that include this track
    playlist_ids = UserVibePlaylist.objects.filter(
        user_vibe__in=user_vibes,
        playlist__trackplaylist__track=track
    ).values_list('playlist_id', flat=True).distinct()

    print(f"Playlist IDs containing the rated track: {list(playlist_ids)}")


    # Now get all TrackPlaylist entries for these playlists
    txp = TrackPlaylist.objects.filter(playlist_id__in=playlist_ids)

    # Tally how many times each track appears
    annotated_tracks = txp.values('track').annotate(count=Count('track'))

    print(f"Updating coefficients for {len(annotated_tracks)} tracks")


    # Define a sigmoid-like scaling function
    scaling_factor = lambda x: 1 / (1 + (1 / (1 + x))) - 0.5

    # Determine rating scale

    print("right before scaling factor")
    max_value = max([choice[0] for choice in TrackRating.RATING_CHOICES])
    mean_choice_value = sum([choice[0] for choice in TrackRating.RATING_CHOICES]) / len(TrackRating.RATING_CHOICES)
    print("after scaling factor")

    print(f"here is trackrating:", trackrating.rating)
    print(f"max_value: {max_value}, mean_choice_value: {mean_choice_value}")

    # Calculate the rating difference
    like_scaling = float(max_value) - float(trackrating.rating) + 1.0 - mean_choice_value

    print("After like_scaling calculation")

    # Loop and update coefficients
    for entry in annotated_tracks:
        print("got into loop for entry:")
        other_track = Track.objects.get(pk=entry['track'])
        print("processing track")
        for user_vibe in user_vibes:
            coeff, _ = TrackCoefficient.objects.get_or_create(
                track=other_track,
                user=user,
                vibe=user_vibe.vibe
            )
            print("updating coefficient for track")
            coeff.coefficient += scaling_factor(entry['count']) * like_scaling
            coeff.save()
            print("coefficient updated")

    print("popular_relation: finished coefficient updates.")


    return True