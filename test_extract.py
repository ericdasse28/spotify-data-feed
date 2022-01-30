import program.extract as script
import datetime


class TestExtract:
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    def test_retrieve_yesterday_songs(self):
        songs_df = script.Extract.retrieve_yesterday_songs()
        for timestamp in songs_df["timestamp"]:
            assert datetime.datetime.strptime(timestamp, "%Y-%m-%d") < self.yesterday
