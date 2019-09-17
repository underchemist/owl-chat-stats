from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.dateparse import parse_datetime

from owl_chat_stats.core.constants import TEAMS, SEASONS, SEASONS_YEAR_MAP


class Match(models.Model):
    team_one = models.CharField(choices=TEAMS, max_length=255)
    team_two = models.CharField(choices=TEAMS, max_length=255)
    season = models.PositiveIntegerField(default=max(SEASONS))
    stage = models.PositiveIntegerField()
    week = models.PositiveIntegerField()
    day = models.PositiveIntegerField()

    def __str__(self):
        return f"Overwatch League Season {self.season} | Stage {self.stage} Week {self.week} Day {self.day} | {TEAMS[self.team_one]} vs. {TEAMS[self.team_two]}"

    class Meta:
        verbose_name_plural = "matches"


class Video(models.Model):
    data = JSONField()
    match = models.OneToOneField(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def parse_title(self):
        """Parse a string formatted similarly to self.__str__ representation into model fields"""
        pieces = [s.strip() for s in self.data["title"].split("|")]
        pieces.pop(pieces.index("Full Match"))
        for piece in pieces:
            if "vs." in piece:
                teams_str = [p.strip() for p in piece.split("vs.")]
                team_one = TEAMS._human_to_db(teams_str[0])
                team_two = TEAMS._human_to_db(teams_str[1])
            if any(keyword in piece for keyword in ("Stage", "Week", "Day")):
                try:
                    stage, week, day = piece.split()[1::2]
                except ValueError:
                    return None

        return {
            "team_one": team_one,
            "team_two": team_two,
            "stage": stage,
            "week": week,
            "day": day,
        }

    def calculate_season(self):
        """Attempt to determine OWL season from publish date"""
        dt = parse_datetime(self.data["published_at"])
        try:
            return SEASONS_YEAR_MAP[dt.year]
        except KeyError:
            return None


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

    def __str__(self):
        return f"<{self.data['commenter']['display_name']}>: {self.data['message']['body']}"
