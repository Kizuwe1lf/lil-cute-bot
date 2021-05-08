import os
import json
import requests
from dotenv import load_dotenv, find_dotenv

class OsuApiUrl:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.api_key = os.getenv('API_KEY')
        self.base_api = "https://osu.ppy.sh/api/"
        self.recent_api_url = self.base_api + "get_user_recent"
        self.user_api_url = self.base_api + "get_user"
        self.beatmap_api_url = self.base_api + "get_beatmaps"
        self.user_best_url = self.base_api + "get_user_best"
        self.beatmap_scores = self.base_api + "get_scores"

    def get_user_recent(self, osu_user):
        recent_url = f"{self.recent_api_url}?k={self.api_key}&u={osu_user}&limit=50"
        try:
            r = requests.get(recent_url)
            j = json.loads(r.content)
            return j
        except:
            return []

    def get_user(self, osu_user):
        user_url = f"{self.user_api_url}?u={osu_user}&k={self.api_key}"
        try:
            r = requests.get(user_url)
            j = json.loads(r.content)
            return j
        except:
            return []

    def get_beatmaps(self, beatmap_id):
        beatmap_url = f"{self.beatmap_api_url}?k={self.api_key}&b={beatmap_id}&mods=0"
        try:
            r = requests.get(beatmap_url)
            j = json.loads(r.content)
            return j
        except:
            return []

    def get_scores(self, osu_user, beatmap_id):
        get_scores_url = f"{self.beatmap_scores}?k={self.api_key}&b={beatmap_id}&u={osu_user}"
        try:
            r = requests.get(get_scores_url)
            j = json.loads(r.content)
            return j
        except:
            return []

    def get_user_best(self, osu_user):
        get_user_best_url = f"{self.user_best_url}?u={osu_user}&k={self.api_key}&limit=100"
        try:
            r = requests.get(get_user_best_url)
            j = json.loads(r.content)
            return j
        except:
            return []

    def get_global(self, beatmap_id, mods):
        if mods != "":
            get_scores_url = f"{self.beatmap_scores}?k={self.api_key}&b={beatmap_id}&mods={mods}&limit=100"
        else:
            get_scores_url = f"{self.beatmap_scores}?k={self.api_key}&b={beatmap_id}&limit=100"
        try:
            r = requests.get(get_scores_url)
            j = json.loads(r.content)
            return j
        except:
            return []


class ApiRequest:
    def __init__(self):
        self.beatmap_id = {}
        self.api = OsuApiUrl()

    def get_beatmap_id(self, channel_id):
        try:
            return self.beatmap_id[channel_id]
        except:
            return []

    def get_scores(self, osu_user, beatmap_id, channel_id):
        self.beatmap_id[channel_id] = beatmap_id
        owo = self.api.get_scores(osu_user, beatmap_id)
        return owo

    def get_user_recent(self, osu_user):
        owo = self.api.get_user_recent(osu_user)
        return owo

    def get_beatmaps_osutop_edition(self, beatmap_id):
        owo = self.api.get_beatmaps(beatmap_id)
        return owo

    def get_scores_osutop_edition(self, osu_user, beatmap_id):
        owo = self.api.get_scores(osu_user, beatmap_id)
        return owo

    def get_beatmaps(self, beatmap_id, channel_id):
        self.beatmap_id[channel_id] = beatmap_id
        owo = self.api.get_beatmaps(beatmap_id)
        return owo

    def get_user(self, osu_user):
        owo = self.api.get_user(osu_user)
        return owo

    def get_user_best1(self, osu_user):
        owo = self.api.get_user_best(osu_user)
        return owo

    def get_global(self, beatmap_id, mods):
        owo = self.api.get_global(beatmap_id, mods)
        return owo
