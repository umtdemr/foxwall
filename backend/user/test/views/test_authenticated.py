def test_update_profile(
    valid_user_profile,
    api_client
):
    api_endpoint = "/user/update/"

    client = api_client()
    client.login(
        username="mediumgoal",
        password="password",
    )
    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + valid_user_profile.user.token
    )

    client.patch(api_endpoint, {"q": "s"})
    assert 0
