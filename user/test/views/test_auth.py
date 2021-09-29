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
        ("test@st.com", "tst", "desiasfre", "Ümit Demir", False, False, False),
        (None, "tst", "denemesifre", "Ümit Demir", False, True, True),
        ("test@test.com", "tst", "password", "Ümit Demir", True, True, False),
        ("test@test.com", "tst", "=9smksd+-", "Ümit<Demir", True, True, False),
        ("test@test.com", "tst", None, "Ümit Demir", True, True, True),
        ("test@test.com", "tst", "x13j", "Ümit Demir", True, True, False),
        (
            "test@test.com",
            "mediumgoal",
            "x1qweqw3j",
            "Ümit Demir",
            True,
            True,
            False
        ),
        (
            "deneme@w.com",
            "qweqwe",
            "x1qweqw3j",
            "Ümit Demir",
            True,
            True,
            False
        ),
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
            api_client().post("/user/register/", register_data)
    else:
        response = api_client().post("/user/register/", register_data)
        print(response)
        print(response.status_code)
        print(response.data)

        if is_error:
            assert response.status_code == 400
        else:
            assert response.status_code == 201


class TestResetPassword:
    request_end_point = "/user/password-reset-request/"
    verify_end_point = "/user/reset-password/"

    def test_reset_password_request_view(
        self,
        api_client,
        valid_user,
    ):
        client = api_client()

        response = client.post(
            "/user/password-reset-request/",
            {
                "email": valid_user.email,
            }
        )

        assert response.data.get("sent")

    def test_password_reset_verify_view(
        self,
        api_client,
        valid_user
    ):
        client = api_client()

        token = valid_user._generate_password_request_token()
        response = client.post(
            self.verify_end_point,
            {
                "token": token,
                "new_password": "yenibirsifre",
            }
        )

        assert response.status_code == 200
        assert "password updated" in response.data.get("message")
