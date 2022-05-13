from spotify_feed.extractor.tracks import get_recent_tracks, request_tracks_prior_to


def test_request_recently_played_tracks_before_a_date():
    data = get_recent_tracks(before="2022-05-03", limit=10)
    assert data, "Unexpectedly get no songs before May 3rd, 2022"
    assert (
        "error" not in data.keys()
    ), "There was an error while retrieving played tracks"
    assert data["limit"] == 10
    assert len(data["items"]) == 10


def test_request_use_cache():
    _ = request_tracks_prior_to(before="2022-05-03", limit=10)
    response_2 = request_tracks_prior_to(before="2022-05-03", limit=10)

    assert response_2.from_cache
