import os

import dotenv

dotenv.load_dotenv()


# Spotify API
SPOTIFY_TOKEN = os.environ.get("TOKEN")
SPOTIFY_ENDPOINT = os.environ.get("ENDPOINT")
SPOTIFY_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SPOTIFY_TOKEN}",
}
