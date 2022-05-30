from django.db import models


class MyPlayedTracks(models.Model):
    song_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    played_at = models.CharField(max_length=200, unique=True)
    timestamp = models.CharField(max_length=200)
