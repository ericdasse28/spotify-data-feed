import datetime

from spotify_feed.extractor.tracks import get_recent_tracks, request_tracks_prior_to


def test_request_recently_played_tracks_before_a_date():
    data = get_recent_tracks(before="2022-05-03", limit=10)
    reference_date = datetime.datetime.strptime("2022-05-03", "%Y-%m-%d")
    assert data, "Unexpectedly get no songs before May 3rd, 2022"
    assert (
        "error" not in data.keys()
    ), "There was an error while retrieving played tracks"
    assert data["limit"] == 10
    data_items = data["items"]
    assert len(data_items) == 10
    for data_item in data_items:
        played_at_day = data_item["played_at"][:10]
        assert datetime.datetime.strptime(played_at_day, "%Y-%m-%d") <= reference_date


def test_request_use_cache():
    _ = request_tracks_prior_to(before="2022-05-03", limit=10)
    response_2 = request_tracks_prior_to(before="2022-05-03", limit=10)

    assert response_2.from_cache

