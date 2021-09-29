from typing import TYPE_CHECKING

from like.models import Like
from post.models import Post


if TYPE_CHECKING:
    from user.models import User


def toggle_like_on_post(post: "Post", user: "User"):
    if not is_user_liked_post(post, user):
        Like.create_like(
            user.id,
            post.id
        )
        return "liked"
    else:
        Like.delete_like(
            user.id,
            post.id
        )
        return "unliked"


def is_user_liked_post(post: "Post", user: "User"):
    return Like.objects.filter(
        post=post,
        user=user
    ).exists()
