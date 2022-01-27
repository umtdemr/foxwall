from typing import TYPE_CHECKING

from rest_framework.fields import ReadOnlyField

from like.utils.crud import is_user_liked_post


if TYPE_CHECKING:
    from post.models import Post


class IsCurrentUserLikedField(ReadOnlyField):
    def __init__(self, **kwargs):
        kwargs["source"] = "pk"
        return super(IsCurrentUserLikedField, self).__init__(**kwargs)

    def to_representation(self, value: "Post"):
        request = self.context.get("request")

        if not request.user.is_anonymous:
            return is_user_liked_post(value, request.user)
        return False
