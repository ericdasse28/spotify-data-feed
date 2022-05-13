import datetime
import os

import dotenv
import requests
import requests_cache

dotenv.load_dotenv()
requests_cache.install_cache(
    "datafeed_cache",
    backend="redis",
    expire_after=180,
)


def get_recent_tracks(before=None, limit=10):
    response = request_tracks_prior_to(before, limit)

    data = response.json()

    return data


def request_tracks_prior_to(before, limit):
    token = os.environ.get("TOKEN")
    endpoint = os.environ.get("ENDPOINT")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    if before:
        date = datetime.datetime.strptime(before, "%Y-%m-%d")
    else:
        date = datetime.datetime.now()
    unix_timestamp = int(date.timestamp()) * 1000

    response = requests.get(
        url=f"{endpoint}?limit={limit}&before={unix_timestamp}",
        headers=headers,
    )

    return response
