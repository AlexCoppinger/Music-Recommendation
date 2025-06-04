from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from .models import Track

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class TrackRatingForm(forms.Form):
    track = forms.ModelChoiceField(queryset=Track.objects.all(), widget=forms.HiddenInput())
    like_rating = forms.IntegerField(min_value=1, max_value=5)
    purpose_rating = forms.IntegerField(min_value=1, max_value=5)