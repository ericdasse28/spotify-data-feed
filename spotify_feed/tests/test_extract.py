import datetime

from spotify_feed.extractor.tracks import (
    get_recent_tracks,
    request_tracks_after,
    request_tracks_prior_to,
)
from spotify_feed.tests.helpers import Context


def test_request_recently_played_tracks_before_a_date():
    context = Context()
    data = get_recent_tracks(before=context.reference_day, limit=10)

    assert data, f"Unexpectedly get no songs before {context.reference_date_str}"
    assert (
        "error" not in data.keys()
    ), "There was an error while retrieving played tracks"

    data_items = data["items"]
    assert data["limit"] == 10
    assert len(data_items) == 10
    for data_item in data_items:
        played_at_day = data_item["played_at"][:10]
        assert (
            datetime.datetime.strptime(played_at_day, "%Y-%m-%d")
            <= context.reference_date
        )


def test_request_recently_played_tracks_after_a_date():
    context = Context()
    data = get_recent_tracks(after=context.reference_day, limit=10)

    assert data, f"Unexpectedly get no songs after {context.reference_date_str}"
    assert (
        "error" not in data.keys()
    ), "There was an error while retrieving played tracks"

    data_items = data["items"]
    assert data["limit"] == 10
    assert len(data_items) == 10
    for data_item in data_items:
        played_at_day = data_item["played_at"][:10]
        assert (
            datetime.datetime.strptime(played_at_day, "%Y-%m-%d")
            >= context.reference_date
        )


def test_request_use_cache():
    context = Context()
    _ = request_tracks_prior_to(before=context.reference_day, limit=10)
    response_2 = request_tracks_prior_to(before=context.reference_day, limit=10)

    assert response_2.from_cache

    _ = request_tracks_after(after=context.reference_day, limit=10)
    response_2 = request_tracks_after(after=context.reference_day, limit=10)

    assert response_2.from_cache
