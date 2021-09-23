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
    print(response.data.get("user"))
    assert response.data.get("user").get("is_following")
    assert response.data.get("user").get("is_followed_me")
