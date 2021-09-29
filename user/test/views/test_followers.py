import pytest

from tests.helpers import login_with_client


@pytest.mark.parametrize(
    "q, count",
    [
        (None, 1),
        ("mediumgoals", 1),
        ("person who is not in followers", 0)
    ]
)
def test_followers_api_view(
    q,
    count,
    follow_obj,
    api_client
):
    client = login_with_client(api_client(), follow_obj.followed_user.token)

    if q:
        response = client.get("/user/followers/", data={"q": q})
    else:
        response = client.get("/user/followers/")

    assert response.status_code == 200
    assert response.data.get("count") == count


@pytest.mark.parametrize(
    "q, count",
    [
        (None, 1),
        ("mediumgoal", 1),
        ("person who is not in followers", 0)
    ]
)
def test_follows_api_view(
    q,
    count,
    follow_obj,
    api_client
):
    client = login_with_client(api_client(), follow_obj.user.token)

    response = client.get("/user/follows/")

    assert response.status_code == 200
    assert response.data.get("count") == 1
