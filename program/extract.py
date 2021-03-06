import datetime
import pandas as pd
import requests
import os


class Extract:
    def __init__(self):

        token = os.environ.get("SPOTIFY_API_KEY")

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self.today = datetime.datetime.now()

    def retrieve_songs(
        self, reference_date: str = "now", days: int = 30
    ) -> pd.DataFrame:
        """Retrieve songs that were listened on Spotify prior to a specific
        time within a time range"""

        if reference_date == "now":
            reference_date_object = self.today
        else:
            reference_date_split = [int(x) for x in reference_date.split("/")]
            reference_date_object = datetime.datetime(
                reference_date_split[2],
                reference_date_split[1],
                reference_date_split[0],
            )

        # The Spotify API will render every song AFTER a specified timestamp
        # For that reason, we should request the songs with the timestamp of
        # the day before the target date, hence days+1 below
        past_date = reference_date_object - datetime.timedelta(days=days + 1)
        past_date_timestamp_ms = int(past_date.timestamp()) * 1000
        request_url = f"https://api.spotify.com/v1/me/player/recently-played?after={past_date_timestamp_ms}"

        # Request to Spotify
        r = requests.get(
            request_url,
            headers=self.headers,
        )

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
            "timestamp": timestamps,
        }

        return pd.DataFrame(song_dict)

    def retrieve_yesterday_songs(self) -> pd.DataFrame:
        """Retrieve songs listened to since yesterday"""

        return self.retrieve_songs(days=1)
