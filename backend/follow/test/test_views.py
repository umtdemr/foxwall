from tests.helpers import login_with_client


def test_user_can_follow_request(
    valid_user,
    valid_user2,
    api_client,
):
    client = login_with_client(
        api_client(),
        valid_user
    )

    response = client.post("/follow/request/", {
        "username": valid_user2.username,
    })

    assert response.status_code == 201
    assert response.data.get("message") == "created"
