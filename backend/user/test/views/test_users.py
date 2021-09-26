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
    assert response.data.get("user").get("is_following") is True
    assert response.data.get("user").get("is_followed_me") is True
    assert response.data.get("user").get("is_sent_follow_request") is False
    assert response.data.get("user").get("is_came_follow_request") is False


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
