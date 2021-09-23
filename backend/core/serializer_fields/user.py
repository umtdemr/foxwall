from typing import TYPE_CHECKING

from rest_framework.fields import ReadOnlyField


if TYPE_CHECKING:
    from user.models import User


class IsFollowingField(ReadOnlyField):
    def __init__(self, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super(IsFollowingField, self).__init__(**kwargs)

    def to_representation(self, value: "User"):
        request = self.context.get('request')
        if not request.user.is_anonymous:
            if request.user.pk == value.pk:
                return False
            return request.user.is_following_with_id(value.pk)

        return False
