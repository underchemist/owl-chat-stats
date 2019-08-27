from django.db import models
from django.contrib.postgres.fields import JSONField

from owl_chat_stats.core.constants import TEAMS, SEASONS


class Match(models.Model):
    team_one = models.CharField(choices=TEAMS, max_length=255)
    team_two = models.CharField(choices=TEAMS, max_length=255)
    season = models.PositiveIntegerField(default=max(SEASONS))
    stage = models.PositiveIntegerField()
    week = models.PositiveIntegerField()
    day = models.PositiveIntegerField()


class Video(models.Model):
    data = JSONField()
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = JSONField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
