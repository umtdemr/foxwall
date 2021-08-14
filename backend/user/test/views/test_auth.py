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


@pytest.mark.parametrize(
    "email, username, password, name, is_cover, is_error, is_throw",
    [
        ("test@test.com", "tst", "emesifre", "Ümit Demir", True, False, False),
        ("test@test.com", "tst", "desifre", "Ümit Demir", False, False, False),
        (None, "tst", "denemesifre", "Ümit Demir", False, True, True),
        ("test@test.com", "tst", "password", "Ümit Demir", True, True, False),
        ("test@test.com", "tst", "=9smksd+-", "Ümit<Demir", True, True, False),
        ("test@test.com", "tst", None, "Ümit Demir", True, True, True),
        ("test@test.com", "tst", "x13j", "Ümit Demir", True, False, False),
    ]
)
def test_register(
    email,
    username,
    password,
    name,
    is_cover,
    is_error,
    is_throw,
    image,
    media_root,
    api_client,
    valid_user,
):
    register_data = {
        "email": email,
        "username": username,
        "password": password,
        "name": name,
    }

    if is_cover:
        register_data["cover"] = image
    if is_throw:
        with pytest.raises(TypeError):
            response = api_client().post("/user/register/", register_data)
    else:
        response = api_client().post("/user/register/", register_data)
        print(response)

        if is_error:
            assert response.status_code == 400

        print(response)
        print(response.status_code)
        print(response.data)
