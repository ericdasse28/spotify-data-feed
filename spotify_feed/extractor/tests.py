from spotify_feed.extractor.tracks import get_recent_tracks


def test_request_recently_played_tracks_before_a_date():
    data = get_recent_tracks(before="2022-05-03", limit=10)
    assert data, "Unexpectedly get no songs before May 3rd, 2022"
    assert (
        "error" not in data.keys()
    ), "There was an error while retrieving played tracks"
    assert data["limit"] == 10
    assert len(data["items"]) == 10
