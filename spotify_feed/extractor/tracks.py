import datetime
from dataclasses import dataclass

import requests
import requests_cache
from spotify_feed.extractor import credentials

requests_cache.install_cache(
    "datafeed_cache",
    backend="redis",
    expire_after=180,
)


@dataclass
class Track:
    song_name: str
    artist_name: str
    played_at: str
    timestamp: str


def get_recent_tracks(*, before=None, after=None, limit=10):
    """
    Gets the most recently played tracks of the current user from the Spotify API.

    Parameters
    ----------
    before: str, optional
        Date of reference before which the tracks were played. Formatted YYYY-mm-dd
        (Default, None)
        Ex. "2022-05-03"
    after: str, optional
        Date of reference after which the tracks were played. Formatted YYYY-mm-dd
        (Default, None)
    limit: int, optional
        Maximum number of tracks to recover (default, 10)

    Returns
    -------
    data: dict
        Dictionary containing raw JSON data about the most recently played tracks.
    """
    if before and after:
        raise AssertionError("You shouldn't define both before and after parameters")

    if after:
        response = request_tracks_after(after, limit=limit)
    else:
        response = request_tracks_prior_to(before, limit=limit)

    data = response.json()

    return data


def request_tracks_prior_to(before, limit):
    if before:
        date = datetime.datetime.strptime(before, "%Y-%m-%d")
    else:
        date = datetime.datetime.now()
    unix_timestamp = int(date.timestamp()) * 1000

    response = requests.get(
        url=f"{credentials.SPOTIFY_ENDPOINT}?limit={limit}&before={unix_timestamp}",
        headers=credentials.SPOTIFY_HEADERS,
    )

    return response


def request_tracks_after(after, limit):
    if after:
        date = datetime.datetime.strptime(after, "%Y-%m-%d")
    else:
        date = datetime.datetime.now()
    unix_timestamp = int(date.timestamp()) * 1000

    response = requests.get(
        url=f"{credentials.SPOTIFY_ENDPOINT}?limit={limit}&after={unix_timestamp}",
        headers=credentials.SPOTIFY_HEADERS,
    )

    return response


def transform(data):
    transformed_tracks = []

    for raw_track in data["items"]:
        transformed_track = Track(
            song_name=raw_track["track"]["name"],
            artist_name=raw_track["track"]["album"]["artists"][0]["name"],
            played_at=raw_track["played_at"][:10],
            timestamp=raw_track["played_at"],
        )
        transformed_tracks.append(transformed_track)

    return transformed_tracks
