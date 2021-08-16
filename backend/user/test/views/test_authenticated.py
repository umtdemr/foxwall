import pytest

from tests.helpers import login_with_client


@pytest.mark.parametrize(
    "bio, is_cover, is_avatar, is_hidden",
    [
        (
            "Example Bio",
            True,
            True,
            True
        ),
        (
            None,
            True,
            True,
            True
        ),
        (
            "qweqwe",
            False,
            True,
            True
        ),
        (
            None,
            True,
            False,
            True
        ),
        (
            None,
            True,
            True,
            None
        ),
        (
            "selam",
            False,
            False,
            False
        ),
    ]
)
def test_update_profile(
    bio,
    is_cover,
    is_avatar,
    is_hidden,
    valid_user_profile,
    api_client,
    user_avatar,
    user_cover,
):
    api_endpoint = "/user/update/"

    client = login_with_client(
        api_client(),
        valid_user_profile.user
    )

    data = dict()
    if bio:
        data["bio"] = bio

    if is_cover:
        data["cover"] = user_cover
    if is_avatar:
        data["avatar"] = user_avatar

    if is_hidden is not None:
        data["is_hidden"] = is_hidden

    response = client.patch(api_endpoint, data)

    assert response.status_code == 200

    response_data = response.data

    assert response_data.get("updated")
    assert 0
