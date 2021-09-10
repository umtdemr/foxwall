from tests.helpers import login_with_client


def test_share_post(
    api_client,
    valid_user_profile
):
    client = login_with_client(
        api_client(),
        valid_user_profile.user.token
    )

    response = client.post("/post/create/", data={})

    assert response.status_code == 200
