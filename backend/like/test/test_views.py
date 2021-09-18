import pytest

from tests.helpers import login_with_client
from like.models import Like


pytestmark = pytest.mark.django_db


def test_like_post(
    api_client,
    valid_user_profile,
    post_obj
):
    client = login_with_client(
        api_client(),
        valid_user_profile.user.token
    )

    response = client.post("/like/action/", {"uuid": post_obj.uuid})

    assert response.status_code == 201
    assert Like.objects.count() == 1
