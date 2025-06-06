# Generated by Django 5.2 on 2025-06-05 11:25

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('spotify_id', models.CharField(max_length=255, unique=True)),
                ('uri', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Playlist',
                'verbose_name_plural': 'Playlists',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('artist', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('album', models.CharField(max_length=255)),
                ('duration_ms', models.IntegerField()),
                ('spotify_id', models.CharField(max_length=255, null=True, unique=True)),
                ('uri', models.CharField(blank=True, max_length=255, null=True)),
                ('preview_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Track',
                'verbose_name_plural': 'Tracks',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Vibe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('algorithm_type', models.CharField(blank=True, max_length=255)),
                ('callback', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('display_name', models.CharField(max_length=255)),
                ('spotify_id', models.CharField(max_length=255, unique=True)),
                ('profile_image', models.URLField(blank=True, null=True)),
                ('uri', models.CharField(blank=True, max_length=255, null=True)),
                ('spotify_access_token', models.CharField(blank=True, max_length=255, null=True)),
                ('spotify_refresh_token', models.CharField(blank=True, max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='custom_user_set', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_user_set', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserVibe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_term', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_vibes', to=settings.AUTH_USER_MODEL)),
                ('vibe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vibe_users', to='vibelink.vibe')),
            ],
            options={
                'unique_together': {('user', 'vibe')},
            },
        ),
        migrations.CreateModel(
            name='PlaylistSearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=255)),
                ('imported_at', models.DateTimeField(auto_now_add=True)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibelink.playlist')),
            ],
            options={
                'unique_together': {('query', 'playlist')},
            },
        ),
        migrations.CreateModel(
            name='TrackPlaylist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibelink.playlist')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibelink.track')),
            ],
            options={
                'unique_together': {('track', 'playlist')},
            },
        ),
        migrations.CreateModel(
            name='TrackRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 'Strongly Agree'), (2, 'Somewhat Agree'), (3, 'Neither Agree nor Disagree'), (4, 'Somewhat Disagree'), (5, 'Strongly Disagree')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibelink.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'track')},
            },
        ),
        migrations.CreateModel(
            name='TrackSearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=255)),
                ('imported_at', models.DateTimeField(auto_now_add=True)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibelink.track')),
            ],
            options={
                'unique_together': {('query', 'track')},
            },
        ),
        migrations.CreateModel(
            name='UserVibePlaylist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibelink.playlist')),
                ('user_vibe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserVibes_playlists', to='vibelink.uservibe')),
            ],
            options={
                'unique_together': {('user_vibe', 'playlist')},
            },
        ),
        migrations.CreateModel(
            name='UserXTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_users', to='vibelink.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tracks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'track')},
            },
        ),
        migrations.CreateModel(
            name='TrackCoefficient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coefficient', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibelink.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vibe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vibelink.vibe')),
            ],
            options={
                'ordering': ['-coefficient'],
                'unique_together': {('track', 'vibe', 'user')},
            },
        ),
    ]
