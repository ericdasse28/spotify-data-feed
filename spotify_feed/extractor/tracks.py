import datetime
import os

import dotenv
import requests

dotenv.load_dotenv()


def get_recent_tracks(before=None, limit=10):
    response = request_previous_tracks(before, limit)

    data = response.json()

    return data


def request_previous_tracks(before, limit):
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
