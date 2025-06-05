from django.shortcuts import render, redirect
from .spotify import import_items
from .spotify import get_spotify_oauth, get_spotify_client, import_playlist_tracks
from .forms import CustomUserCreationForm, TrackRatingForm
from .models import User, Playlist, Track, TrackRating, Vibe, UserVibe, UserVibePlaylist, TrackCoefficient, TrackPlaylist
from .algorithms import popular_relation

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction 

import spotipy 
import uuid
import json

# The following function are irrelevant to our app now
# They're just here for reference:

# def playlist_search_view(request):
#     print("search_spotify_playlists called")
#     query = request.GET.get('query', '')
#     playlists = []
#     if query:
#         try:
#             playlists = search_playlists(query)
#         except Exception as e:
#             return render(request, 'vibelink/search.html', {'error': str(e)})
#     return render(request, 'vibelink/search.html', {'playlists': playlists})

# def track_search_view(request):
#     query = request.GET.get('query', '')
#     tracks = []
#     if query:
#         try:
#             tracks = search_tracks(query)
#         except Exception as e:
#             return render(request, 'vibelink/search.html', {'error': str(e)})
#     return render(request, 'vibelink/search.html', {'tracks': tracks})

def home(request):
    return render(request, 'vibelink/home.html')

# Functions from here on our are relevant to our app
# Spotify login trigger and callback views:

def spotify_login(request):
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url() + f"&state={uuid.uuid4()}"

    next_url = request.GET.get('next')
    if next_url:
        request.session['next_url'] = next_url # Gets the URL the user was trying to access but wasn't logged in for 

    return redirect(auth_url)

def spotify_logout(request):

    if request.user.is_authenticated:
    # Store the Spotify access token to revoke it
        access_token = request.user.spotify_access_token
    
    # logout using Django's logout function stuff
    logout(request)

    response = redirect('vibelink:home')
    response.delete_cookie('sessionid')  # Explicitly delete session cookie because of login issues

    messages.success(request, 'You have been logged out.')
    return response

def spotify_callback(request):
    print("spotify_callback called")

    sp_oauth = get_spotify_oauth()
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        return render(request, "vibelink/error.html", {"message": f"Spotify authorization failed: {error}"})

    if code:
        print(f"Received code: {code}")
        try:
            token_info = sp_oauth.get_access_token(code, as_dict=True)
            request.session['token_info'] = token_info  # Store token info in session
            access_token = token_info['access_token']
            refresh_token = token_info.get('refresh_token')
            print(f"Access token: {access_token}")
            
            sp = spotipy.Spotify(auth=access_token)
            profile = sp.current_user()
            print(f"User profile: {profile}")

            # Get profile image if available
            profile_image_url = None
            if profile['images'] and len(profile['images']) > 0:
                profile_image_url = profile['images'][0]['url'] 
        except Exception as e:
            return render(request, "vibelink/error.html", {"message": f"Spotify token error: {e}"})

        spotify_id = profile['id']
        display_name = profile.get('display_name', '')
        uri = profile.get('uri', '')

        user, created = User.objects.get_or_create(
            spotify_id=spotify_id,
            defaults={
                'display_name': display_name,
                'username': spotify_id,  # Required for AbstractUser
                'uri': uri,
                'spotify_access_token': access_token,
                'spotify_refresh_token': refresh_token,
                'profile_image': profile_image_url, # If there is no spotify image, ChatGPT found a link to a generic one that can be used
            }
        )

        # If the user already existed, update tokens just in case
        if not created:
            user.profile_image = profile_image_url # in case profile image was changed 
            user.spotify_access_token = access_token
            user.spotify_refresh_token = refresh_token
            user.save()

        login(request, user)  # Log the user in using Django's login system and the user's spotify credentials

        next_url = request.session.pop('next_url', None) # Gets the next URL to redirect to that 
        if next_url:
            return redirect(next_url)
        
        return redirect('vibelink:home')    

# Because there keeps being that stupid user error
def refresh_spotify_token(user):
    """Refresh the user's Spotify access token if it has expired"""
    try:
        sp_oauth = get_spotify_oauth()
        if user.spotify_refresh_token:
            token_info = sp_oauth.refresh_access_token(user.spotify_refresh_token)
            user.spotify_access_token = token_info['access_token']
            user.save()
            return True
    except Exception as e:
        print(f"Error refreshing token: {str(e)}")
        return False
    return False

# This gets onto vibes.html and gets all the vibes from the user
@login_required
def vibes_view(request):
    user = request.user # Get the user
    user_vibes = UserVibe.objects.filter(user=user) # Get the vibes from the user

    
    return render(request, 'vibelink/vibes.html', {
        'vibes': user_vibes, # Pass the vibes to the template (if they even have any)
        'has_vibes': user_vibes.exists() # Check if the user even has vibes
    })

# This creates a new vibe from vibes.html on new_vibe.html
@login_required
def new_vibe_view(request):
    user = request.user

    if request.method == 'POST':
        vibe_name = request.POST.get('vibe_name')  # Name for Vibe
        search_term = request.POST.get('search_term')  # Search term for UserVibe
        description = request.POST.get('description')  # Optional description

        if vibe_name and search_term:
            # Create Vibe and UserVibe
            vibe = Vibe.objects.create(name=vibe_name, description=description)
            user_vibe = UserVibe.objects.create(user=user, vibe=vibe, search_term=search_term)

            # Import playlists and tracks from Spotify
            # There seems to be some fishy stuff going on here, but I'll look over it later
            # context = import_items(query=search_term, type='playlist')
            # # Fishy stuff in context right now

            # track_playlists = []  # To store TrackPlaylist objects

            # # Associate playlists with UserVibe
            # for playlist in context['playlists']:
            #     UserVibePlaylist.objects.get_or_create(
            #         playlist=playlist,
            #         defaults={'user_vibe': user_vibe}
            #     )

            #     # Import tracks from playlists and create TrackPlaylist objects
            #     track_playlists.extend(import_playlist_tracks(playlist))

            context = import_items(query=search_term, type='track')
            print(f"list of tracks: {[track.name for track in context['tracks']]}")
            # Associate tracks with "Vibe & User
            track_coefficients = [
                TrackCoefficient(
                    track=track,
                    user=user,
                    vibe=vibe,
                    coefficient=0.0
                )
                for track in context['tracks']
            ]

            print(f"Creating {len(track_coefficients)} TrackCoefficient objects for vibe '{vibe_name}'")

            TrackCoefficient.objects.bulk_create(track_coefficients)

            print("Vibe and coefficients created.")
            return redirect('vibelink:vibes')

    return render(request, 'vibelink/new_vibe.html')

# To update the description of a vibe on vibe_detail.html (this will use other urls, but there is no need for confusion on the user side of things)
@login_required
def update_vibe_description(request, vibe_id):
    """Update the description of a vibe"""
    if request.method == 'POST':
        try:
            # Get the vibe object
            vibe = get_object_or_404(Vibe, id=vibe_id)
            
            # Check if the user has access to this vibe
            user_vibe = UserVibe.objects.filter(user=request.user, vibe=vibe).first()
            if not user_vibe:
                return JsonResponse({'success': False, 'error': 'You do not have access to this vibe'}, status=403)
            
            # Parse the JSON data from the request
            data = json.loads(request.body)
            new_description = data.get('description', '')
            
            # Update the vibe description
            vibe.description = new_description
            vibe.save()
            
            return JsonResponse({'success': True}) # Apparently this is useful
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500) # And this
            
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405) # And this

# To access the details of a vibe on vibe_detail.html
@login_required
def vibe_detail_view(request, vibe_name):
    # Get the user and vibe objects
    user = request.user
    
    # First try to get the UserVibe object which contains the relationship
    user_vibe = get_object_or_404(UserVibe, user=user, vibe__name=vibe_name)

    request.session['selected_vibe'] = user_vibe.vibe.id  # Store the selected vibe ID in the session
    
    # Pass both the vibe and the user_vibe to the template
    return render(request, 'vibelink/vibe_detail.html', {
        'vibe': user_vibe.vibe, 
        'description': user_vibe.vibe.description, # This is the description of the vibe
        'user_vibe': user_vibe, # This may be unnecessary
        'search_term': user_vibe.search_term # This may also be unnecessary
    })

# To delete a vibe on the vibes page
@login_required
def delete_vibe_view(request, uservibe_id):
    user_vibe = get_object_or_404(UserVibe, id=uservibe_id, user=request.user)
    if request.method == 'POST':
        vibe = user_vibe.vibe
        user_vibe.delete()

        if not UserVibe.objects.filter(vibe=vibe).exists():
            vibe.delete()

    return redirect('vibelink:vibes')

# Onwards is a bunch of stuff related to playing/rating tracks:

@login_required
def play_track(request):
    if request.method == 'POST':
        try:
            refresh_spotify_token(request.user)

            data = json.loads(request.body)
            track_id = data.get('track_id')
            print("Track ID received:", track_id)

            track = Track.objects.get(id=track_id)
            print("Found track:", track.name)

            sp = get_spotify_client(request)
            print("Spotify client retrieved")
            print("Token info from request:", request.session.get("token_info"))

            # For debugging purposes
            try:
                user = sp.current_user()
                print("Logged in as:", user['display_name'], "| ID:", user['id'])
            except Exception as e:
                print("Failed to get user profile:", e)


            devices = sp.devices().get('devices', [])
            print("Devices:", devices)

            if not devices:
                return JsonResponse({'success': False, 'error': 'No active Spotify device found'}, status=400)

            active_device = next((d for d in devices if d['is_active']), None)
            device_id = active_device['id'] if active_device else devices[0]['id']

            print("Selected device ID:", device_id)

            sp.transfer_playback(device_id=device_id, force_play=True)
            sp.start_playback(device_id=device_id, uris=[track.uri])

            return JsonResponse({'success': True})

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
def submit_rating(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            track_id = data.get('track_id')
            rating_value = data.get('rating')
            vibe_id = request.session.get('selected_vibe')
            
            if not track_id or not rating_value:
                return JsonResponse({'success': False, 'error': 'Missing track_id or rating'}, status=400)
            
            track = Track.objects.get(id=track_id)
            
            # Save or update the rating
            rating, created = TrackRating.objects.update_or_create(
                user=request.user,
                track=track,
                defaults={'rating': rating_value}
            )
            
            # Store the last rated track ID in session
            request.session['last_rated_track_id'] = track_id
            
            # Get next unrated track
            if vibe_id:
                vibe = Vibe.objects.get(id=vibe_id)
                
                # Get the count of tracks rated so far for this vibe
                rated_count = TrackRating.objects.filter(
                    user=request.user,
                    track__trackcoefficient__vibe=vibe
                ).count()
                
                # Get total tracks for this vibe
                total_tracks = TrackCoefficient.objects.filter(
                    vibe=vibe,
                    user=request.user
                ).count()
                
                # Check if there are more tracks to rate
                next_track_available = rated_count < total_tracks
                
                return JsonResponse({
                    'success': True,
                    'message': 'Rating saved',
                    'created': created,
                    'next_track_available': next_track_available,
                    'rated_count': rated_count,
                    'total_tracks': total_tracks
                })
            
            return JsonResponse({
                'success': True, 
                'message': 'Rating saved',
                'created': created
            })
            
        except Track.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Track not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

@login_required
def rate_song_view(request):
    user = request.user
    
    # Get the vibe ID from the session
    vibe_id = request.session.get('selected_vibe')
    
    if not vibe_id:
        messages.error(request, "Please select a vibe first")
        return redirect('vibelink:vibes')
    
    # Get the vibe
    vibe = get_object_or_404(Vibe, id=vibe_id)
    
    # Get the ID of the last rated track (if any)
    last_rated_track_id = request.session.get('last_rated_track_id')
    
    # Get all tracks for this vibe that haven't been rated by this user yet
    rated_track_ids = TrackRating.objects.filter(
        user=user,
        track__trackcoefficient__vibe=vibe
    ).values_list('track_id', flat=True)
    
    # Get a track coefficient that hasn't been rated yet
    track_coefficient = TrackCoefficient.objects.filter(
        vibe=vibe,
        user=user
    ).exclude(
        track_id__in=rated_track_ids
    ).first()
    
    if not track_coefficient:
        messages.info(request, "You've rated all tracks for this vibe!")
        return redirect('vibelink:vibe_detail', vibe_name=vibe.name)
    
    # Store vibe ID in session for next track
    request.session['selected_vibe'] = vibe_id
    
    return render(request, 'vibelink/rate.html', {
        'track': track_coefficient.track,
        'vibe': vibe,
        'rating_count': len(rated_track_ids),
        'total_tracks': TrackCoefficient.objects.filter(vibe=vibe, user=user).count()
    })
