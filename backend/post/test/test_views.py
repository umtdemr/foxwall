import pytest

from post.models import Post
from tests.helpers import login_with_client


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "text, is_image, is_error",
    [
        (
            "bu bir post denemesidir",
            True,
            False
        ),
        (
            "bu bir post denemesidir",
            False,
            False
        ),
        (
            "",
            True,
            False
        ),
        (
            "",
            False,
            True
        )
    ]
)
def test_share_post(
    text,
    is_image,
    is_error,
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
        "text": text,
    }
    if is_image:
        post_data["image"] = user_cover

    response = client.post("/post/create/", post_data)

    if is_error:
        assert response.status_code == 400
    else:
        assert response.status_code == 201


def test_delete_post_view(
    api_client,
    post_obj
):
    client = login_with_client(
        api_client(),
        post_obj.user.token
    )

    response = client.delete(f"/post/delete/{post_obj.uuid}/")

    assert response.status_code == 204
    assert Post.objects.all().count() == 0


def test_only_owner_can_delete_post(
    api_client,
    post_obj,
    valid_user2
):
    client = login_with_client(
        api_client(),
        valid_user2.token
    )

    response = client.delete(f"/post/delete/{post_obj.uuid}/")

    assert response.status_code == 403
