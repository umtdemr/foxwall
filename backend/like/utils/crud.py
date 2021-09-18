from re import M
from typing import TYPE_CHECKING

from like.models import Like
from post.models import Post


if TYPE_CHECKING:
    from user.models import User


def toggle_like_on_post(post: "Post", user: "User"):
    pass
