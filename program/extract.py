import datetime
import pandas as pd
import requests
from dateutil.parser import parse


class Extract:

    TOKEN = "BQABeZW8OAQ2nL6psqo4XTf_oXUKr1KKsqU-1hlLeB6siKc_6M0BJhB8LpyAPY3oAo4WCKeMZ581fZR_jP_EZc9DKW7kZF7hxf7Snc95q2yS9sKEHtIDcWfCoc99Hdky7inSK4YpEdXxyBoIfs-S"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }
    today = datetime.datetime.now()

    def retrieve_songs(self, reference_date="now", days=30) -> pd.DataFrame:
        """Retrieve songs that were listened on Spotify prior to a specific time within a time range"""
        if reference_date == "now":
            reference_date_object = self.today
        else:
            reference_date_split = list(map(int, reference_date.split("/")))
            reference_date_object = datetime.datetime(reference_date_split[2],
                                                      reference_date_split[1],
                                                      reference_date_split[0])

        past_date = reference_date_object - datetime.timedelta(days=days)
        past_date_timestamp_ms = int(past_date.timestamp()) * 1000

        # Request to Spotify
        r = requests\
            .get("https://api.spotify.com/v1/me/player/recently-played?after={time}"
                 .format(time=past_date_timestamp_ms), headers=self.headers)

        data = r.json()

        song_names = []
        artist_names = []
        played_at_list = []
        timestamps = []

        for song in data["items"]:
            song_names.append(song["track"]["name"])
            artist_names.append(song["track"]["album"]["artists"][0]["name"])
            played_at_list.append(song["played_at"])
            timestamps.append(song["played_at"][:10])

        song_dict = {
            "song_name": song_names,
            "artist_name": artist_names,
            "played_at": played_at_list,
            "timestamp": timestamps
        }

        return pd.DataFrame(song_dict)

    def retrieve_yesterday_songs(self) -> pd.DataFrame:
        """Retrieve songs listened to since yesterday"""

        return self.retrieve_songs(days=1)
