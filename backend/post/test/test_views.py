from tests.helpers import login_with_client


def test_share_post(
    api_client,
    valid_user_profile,
    user_cover,
    media_root
):
    client = login_with_client(
        api_client(),
        valid_user_profile.user.token
    )

    post_data = {
        "text": "Bu bir post denemesidir",
        "image": user_cover
    }

    response = client.post("/post/create/", post_data)

    assert response.status_code == 200
