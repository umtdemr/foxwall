from tests.helpers import login_with_client


def test_followers_api_view(follow_obj, api_client):
    client = login_with_client(api_client(), follow_obj.followed_user.token)

    response = client.get("/user/followers/")

    assert response.status_code == 200


def test_follows_api_view(follow_obj, api_client):
    client = login_with_client(api_client(), follow_obj.user.token)

    response = client.get("/user/follows/")

    assert response.status_code == 200
