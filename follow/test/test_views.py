import pytest
from typing import TYPE_CHECKING

from tests.helpers import login_with_client


if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "creator, target, status_code",
    [
        (
            "valid_user",
            "valid_user2",
            201
        ),
        (
            "valid_user2",
            "valid_user2",
            400
        ),
        (
            "valid_user2",
            "s",
            400
        ),
    ]
)
def test_user_can_follow_request(
    creator,
    target,
    status_code,
    api_client,
    request: "FixtureRequest",
):
    creator = request.getfixturevalue(creator)
    try:
        target = request.getfixturevalue(target)
        target_username = target.username
    except Exception:
        target_username = "not_exist_username"
    client = login_with_client(
        api_client(),
        creator.token
    )

    response = client.post("/follow/request/", {
        "username": target_username,
    })

    assert response.status_code == status_code


def test_cancel_follow_request_view(
    valid_user,
    valid_user2,
    follow_request_obj,
    api_client,
):
    client = login_with_client(
        api_client(),
        valid_user.token
    )

    response = client.post(
        "/follow/cancel-request/",
        {
            "username": valid_user2.username
        }
    )

    assert response.status_code == 200


def test_received_follow_requests_view(
    follow_request_obj,
    api_client
):

    client = login_with_client(
        api_client(),
        follow_request_obj.target_user.token
    )

    response = client.get(
        "/follow/received-requests/",
    )

    assert response.status_code == 200
    assert response.data.get("count") == 1
    results = response.data.get("results")[0]
    assert follow_request_obj.creator.username in \
        results["creator"]["username"]


def test_reject_follow_request_view(
    follow_request_obj,
    api_client
):
    client = login_with_client(
        api_client(),
        follow_request_obj.target_user.token
    )

    response = client.post(
        "/follow/reject-follow-request/",
        {
            "username": follow_request_obj.creator.username
        }
    )
    assert response.status_code == 200
    assert response.data.get("message") == "rejected"


def test_allow_follow_request_view(
    follow_request_obj,
    api_client
):
    client = login_with_client(
        api_client(),
        follow_request_obj.target_user.token
    )

    response = client.post(
        "/follow/allow-follow-request/",
        {
            "username": follow_request_obj.creator.username
        }
    )

    assert response.status_code == 200
    assert response.data.get("message") == "allowed"


def test_unfollow_view(
    follow_obj,
    api_client
):
    client = login_with_client(
        api_client(),
        follow_obj.user.token
    )

    response = client.post(
        "/follow/unfollow/",
        {
            "username": follow_obj.followed_user.username
        }
    )

    assert response.status_code == 200
    assert response.data.get("message") == "unfollowed"
