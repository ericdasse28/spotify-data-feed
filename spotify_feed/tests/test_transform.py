from spotify_feed.extractor.tracks import Track, get_recent_tracks, transform
from spotify_feed.tests.helpers import Context


def test_format_extracted_data():
    # TODO: Use a parameterized fixture for get_recent_tracks parameters
    context = Context()
    data = get_recent_tracks(before=context.reference_day)

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
