import pytest
from spotify_feed.extractor.tracks import Track, get_recent_tracks, transform
from spotify_feed.tests.helpers import make_test_dates

test_dates = make_test_dates()


@pytest.mark.parametrize("before, after", test_dates)
def test_format_extracted_data(before, after):
    data = get_recent_tracks(before=before, after=after)

    transformed_tracks = transform(data)

    assert isinstance(transformed_tracks, list)
    for i in range(len(data["items"])):
        transformed_track = transformed_tracks[i]
        raw_track = data["items"][i]

        assert isinstance(transformed_track, Track)
        assert transformed_track.song_name == raw_track["track"]["name"]
        assert (
            transformed_track.artist_name
            == raw_track["track"]["album"]["artists"][0]["name"]
        )
        assert transformed_track.played_at == raw_track["played_at"][:10]
        assert transformed_track.timestamp == raw_track["played_at"]


@pytest.mark.parametrize("before, after", test_dates)
def test_timestamps_are_unique(before, after):
    data = get_recent_tracks(before=before, after=after)

    transformed_tracks = transform(data)

    timestamps = []
    for transformed_track in transformed_tracks:
        timestamps.append(transformed_track.timestamp)
    assert len(set(timestamps)) == len(timestamps)
