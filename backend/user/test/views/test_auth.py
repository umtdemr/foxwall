import pytest

from user.models import User

pytestmark = pytest.mark.django_db


class TestLoginAPIView:
    endpoint = "/user/login/"

    def test_login_with_username(self, valid_user2, api_client):
        response = api_client().post(self.endpoint, {
            "username": valid_user2.username,
            "password": "passwsord",
        })
        assert response.status_code == 200
