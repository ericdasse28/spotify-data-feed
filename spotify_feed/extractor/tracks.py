import datetime

import requests
import requests_cache
from spotify_feed.extractor import credentials

requests_cache.install_cache(
    "datafeed_cache",
    backend="redis",
    expire_after=180,
)


def get_recent_tracks(before=None, after=None, limit=10):
    """
    Gets the most recently listened tracks of the user from Spotify API.

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
