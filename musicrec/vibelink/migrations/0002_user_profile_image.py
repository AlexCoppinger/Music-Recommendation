# Generated by Django 5.2 on 2025-05-29 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vibelink', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
