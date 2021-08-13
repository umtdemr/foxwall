import pytest


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "email, username, password, status_code",
    [
        (None, "mediumgoals", "passwsord", 200),
        ("deneme@w.scom", None, "passwsord", 200),
        ("deneme@w.scom", "mediumgoals", "passwsord", 200),
        ("deneme@w.scom", None, "spasswsord", 401),
        (None, None, "passwsord", 400),
    ],
)
def test_login(
    email,
    username,
    password,
    status_code,
    valid_user2,
    api_client,
):
    post_data = {"password": password}
    if username:
        post_data["username"] = username
    if email:
        post_data["email"] = email

    response = api_client().post("/user/login/", post_data)

    assert response.status_code == status_code
    if response.status_code == 200:

        assert response.data.get("email") == valid_user2.email
        assert response.data.get("token") == valid_user2.token
