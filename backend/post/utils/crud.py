from typing import TYPE_CHECKING, Optional, List

from post import PostStatus, PostVisibility
from post.models import Post, PostImage
from core.validators.post import text_or_image_must_required


if TYPE_CHECKING:
    from user.models import User


def create_post(
    user: "User",
    text: str,
    status: PostStatus = PostStatus.PUBLISHED,
    visibility: PostVisibility = PostVisibility.VISIBLE,
    images: Optional[List] = None,
):
    text_or_image_must_required(text, images)
    post = Post(
        user=user,
        text=text,
        status=status,
        visibility=visibility
    )
    post.save()

    if images:
        for image in images:
            PostImage.objects.create(
                post=post,
                image=image["image"]
            )

    return post.uuid
