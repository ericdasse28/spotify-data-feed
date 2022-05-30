import datetime
import os
import sqlite3

import dotenv
import pandas as pd
import requests
import sqlalchemy

dotenv.load_dotenv()

DATABASE_LOCATION = os.environ.get("DATABASE_LOCATION")
USER_ID = os.environ.get("USER_ID")
TOKEN = os.environ.get("TOKEN")


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

    # Primary check
    if not pd.Series(df["played_at"]).is_unique:
        raise IntregrityError("Primary Key Check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null valued found")

    # Check all timestamps are of yesterday's date
    yesterday_time = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_time = yesterday_time.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps_from_df = df["timestamp"].tolist()
    for timestamp in timestamps_from_df:
        if datetime.datetime.strptime(timestamp, "%Y-%m-%d") < yesterday:
            raise Exception(
                "At least one of the returned songs does not come from"
                "the last 24 hours"
            )

    return True


if __name__ == "__main__":

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(
            time=yesterday_unix_timestamp
        ),
        headers=headers,
    )

    data = r.json()

    breakpoint()

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

    song_df = pd.DataFrame(song_dict)

    print(song_df.to_string())

    # Validate
    if check_if_valid_data(song_df):
        print("Data valid, proceed to load stage")

    # Load
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect("my_played_at_tracks.sqlite")
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks (
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists="append")
    except Exception:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")
