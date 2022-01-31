import program.extract as script
import datetime
import pandas as pd


class TestExtract:
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    def test_data_validity(self):
        """Test the validity of the retrieved songs data"""
        songs_df = script.Extract.retrieve_songs()

        # Is the result a Pandas DataFrame?
        assert isinstance(songs_df, pd.DataFrame)
        # Is the dataframe empty?
        if not songs_df.empty:
            # If not, test that the values in the 'played_at' column are unique (primary key check)
            assert pd.Series(songs_df['played_at']).is_unique
            # Test that there aren't any missings values
            assert songs_df.is_null().values.any()

    def test_retrieve_songs_timestamp(self):
        """Test the validity of the timestamp of songs retrieved within a given time period"""
        songs_df = script.Extract.retrieve_songs(start_date="30/11/2022", days=30)
        start_date = datetime.datetime(2022, 11, 31)
        past_date = start_date - datetime.timedelta(days=30)
        for timestamp in songs_df["timestamp"]:
            assert datetime.datetime.strptime(timestamp, "%Y-%m-%d") < past_date

    def test_retrieve_yesterday_songs_timestamp(self):
        """Verify the timestamp is correct when songs from yesterday to now are retrieved"""

        songs_df = script.Extract.retrieve_yesterday_songs()
        for timestamp in songs_df["timestamp"]:
            assert datetime.datetime.strptime(timestamp, "%Y-%m-%d") < self.yesterday
