import os

from ..utils import post_image_upload_directory


def test_post_upload_path(post_img_obj):
    filename = os.path.basename(post_img_obj.image.path)
    path = post_image_upload_directory(
        post_img_obj,
        filename
    )

    assert "posts" in path
    assert str(post_img_obj.post.uuid) in path
