from tests.helpers import login_with_client


def test_update_profile(
    valid_user_profile,
    api_client
):
    api_endpoint = "/user/update/"

    client = login_with_client(
        api_client(),
        valid_user_profile.user
    )

    client.patch(api_endpoint, {"q": "s"})
    assert 0
