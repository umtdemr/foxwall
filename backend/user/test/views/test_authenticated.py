import pytest

from tests.helpers import login_with_client


@pytest.mark.parametrize(
    "bio, is_cover, is_avatar, is_hidden, username",
    [
        (
            "Example Bio",
            True,
            True,
            True,
            "mediumgoal"
        ),
        (
            None,
            True,
            True,
            True,
            "mediumgoal",
        ),
        (
            "qweqwe",
            False,
            True,
            True,
            "mediumgoal"
        ),
        (
            None,
            True,
            False,
            True,
            "mediumgoal"
        ),
        (
            None,
            True,
            True,
            None,
            "mediumgoal"
        ),
        (
            "selam",
            False,
            False,
            False,
            "mediumgoal"
        ),
    ]
)
def test_update_profile(
    bio,
    is_cover,
    is_avatar,
    is_hidden,
    username,
    valid_user_profile,
    api_client,
    user_avatar,
    user_cover,
):
    api_endpoint = "/user/me/"

    client = login_with_client(
        api_client(),
        valid_user_profile.user
    )

    data = dict()

    if username:
        data["username"] = username

    if bio:
        data["bio"] = bio

    if is_cover:
        data["cover"] = user_cover
    if is_avatar:
        data["avatar"] = user_avatar

    if is_hidden is not None:
        data["is_hidden"] = is_hidden

    response = client.patch(api_endpoint, data, "multipart")

    assert response.status_code == 200

    response_data = response.data

    assert response_data.get("updated")


def test_retrieve_me(
    valid_user_profile,
    api_client,
):
    client = login_with_client(
        api_client(),
        valid_user_profile.user
    )

    response = client.get("/user/me/")
    username = response.data.get("username")
    email = response.data.get("email")
    name = response.data.get("name")
    is_celebrity = response.data.get("is_celebrity")
    is_hidden = response.data.get("is_hidden")
    bio = response.data.get("bio")

    assert username == str(valid_user_profile.user)
    assert email == valid_user_profile.user.email
    assert name == valid_user_profile.name
    assert is_celebrity == valid_user_profile.is_celebrity
    assert is_hidden == valid_user_profile.is_hidden
    assert bio == valid_user_profile.bio
