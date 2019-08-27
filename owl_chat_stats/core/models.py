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

    def __str__(self):
        return f"Overwatch League Season {self.season} | Stage {self.stage} Week {self.week} Day {self.day} | {TEAMS[self.team_one]} vs. {TEAMS[self.team_two]}"


class Video(models.Model):
    data = JSONField()
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = JSONField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    _emote_endpoint = "https://static-cdn.jtvnw.net/emoticons/v1/{}/{}"

    def get_twitch_emoticon_url(self, emoticon_id, size="1.0"):
        """Fill in templated emote endpoint to generate emote url"""
        return self._emote_endpoint.format(emoticon_id, size)
