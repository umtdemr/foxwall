from tests.helpers import login_with_client


def test_get_user_api_view(
    api_client,
    follow_obj,
    valid_user,
    valid_user2
):

    client = login_with_client(
        api_client(),
        valid_user2.token,
    )

    response = client.get(f"/user/profile/{valid_user2.username}")

    assert response.status_code == 200
