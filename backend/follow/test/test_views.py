import pytest
from typing import TYPE_CHECKING

from tests.helpers import login_with_client


if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest


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
        creator
    )

    response = client.post("/follow/request/", {
        "username": target_username,
    })

    assert response.status_code == status_code


def test_delete_follow_request_view(
    valid_user,
    valid_user2,
    follow_request_obj,
    api_client,
):
    client = login_with_client(
        api_client(),
        valid_user
    )

    response = client.post(
        "/follow/cancel-request/",
        {
            "userame": valid_user2.username
        }
    )

    assert response.status_code == 200
