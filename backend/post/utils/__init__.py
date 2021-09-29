from typing import TYPE_CHECKING

from core.utils.files import generate_new_filename

if TYPE_CHECKING:
    from post.models import PostImage


def post_image_upload_directory(image_obj: "PostImage", filename: str):
    new_filename = generate_new_filename(filename)

    path = f"posts/{image_obj.post.uuid}/{new_filename}"
    return path
