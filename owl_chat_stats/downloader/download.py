from datetime import timedelta

import twitch
from django.conf import settings
from more_itertools import chunked


class Downloader:

    def __init__(self, client_id=None):
        self._client_id = client_id or settings["TWITCH_CLIENT_ID"]
        self.client = twitch.Helix(self._client_id, use_cache=True, cache_duration=timedelta(minutes=30))
        self.channel = self.client.user("overwatchleague")
        self.videos = self.filter_by_full_matches(self.get_channel_videos({"type": "highlight"}))

    def get_channel_videos(self, params):
        return list(self.channel.videos(**params))

    @staticmethod
    def filter_by_full_matches(videos):
        # keep videos with "Full Match" in title. These are highlights created
        # by overwatchleague twitch channel.
        return list(filter(lambda x: "Full Match" in x.title and x.type == "highlight", videos))

    def stream_comments(self, video, batch_size=1000):
        comments = video.comments
        for chunk in chunked(comments, batch_size):
            yield list(chunk)
