import pytest

from tests.helpers import login_with_client


def test_get_user_api_view(
    api_client,
    follow_obj,
    follow_obj2,
):

    client = login_with_client(
        api_client(),
        follow_obj.user.token,
    )

    response = client.get(
        f"/user/profile/{follow_obj.followed_user.username}/"
    )

    assert response.status_code == 200
    assert response.data.get("is_following") is True
    assert response.data.get("is_followed_me") is True
    assert response.data.get("is_sent_follow_request") is False
    assert response.data.get("is_came_follow_request") is False


def test_get_user_posts_api_view(
    api_client,
    follow_obj,
    post_obj,
):
    client = login_with_client(
        api_client(),
        follow_obj.user.token
    )

    response = client.get(
        f"/user/profile/{follow_obj.followed_user.username}/posts/"
    )

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.parametrize(
    "search_param, status_code",
    [
        ("mediumgoal", 200),
        ("deneme@w.com", 200),
        ("ümit", 200),
        ("no_exist", 404),
        ("qweqewqew@w.com", 404),
        ("john", 404),
    ]
)
def test_user_search_api_view(
    search_param,
    status_code,
    api_client,
    valid_user_profile,
):
    client = api_client()

    response = client.get(
        f"/user/search/?q={search_param}"
    )

    assert response.status_code == status_code
