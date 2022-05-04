import datetime
import os

import dotenv
import requests

dotenv.load_dotenv()


def get_recent_tracks(before=None, limit=10):
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

    r = requests.get(
        url=f"{endpoint}?limit={limit}&before={unix_timestamp}",
        headers=headers,
    )

    data = r.json()

    return data
