# spotify-data-feed
Implementation of a data feed (data pipeline) using Spotify API. This feed runs daily, and downloads the data about the songs that a specific user listened to during the day and save the data in a PostgreSQL database

## Running the program locally
You first to configure a PostgreSQL database through the following commands

```
sudo -u postgres psql

CREATE DATABASE spotify_feed;
CREATE USER spotify WITH ENCRYPTED PASSWORD 'spotify';
GRANT ALL PRIVILEGES ON DATABASE spotify_feed TO spotify;
ALTER ROLE spotify SUPERUSER;
```
