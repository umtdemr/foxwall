from typing import TYPE_CHECKING

from rest_framework.fields import ReadOnlyField


if TYPE_CHECKING:
    from user.models import User


class IsFollowingField(ReadOnlyField):
    def __init__(self, **kwargs):
        kwargs["source"] = "*"
        super(IsFollowingField, self).__init__(**kwargs)

    def to_representation(self, value: "User"):
        request = self.context.get("request")

        if not request.user.is_anonymous:
            if request.user.pk == value.pk:
                return False
            return request.user.is_following_with_id(value.pk)

        return False


class IsFollowedMeField(ReadOnlyField):
    def __init__(self, **kwargs):
        kwargs["source"] = "*"
        return super(IsFollowedMeField, self).__init__(**kwargs)

    def to_representation(self, value: "User"):
        request = self.context.get("request")

        if not request.user.is_anonymous:
            if request.user.pk == value.pk:
                return False
            return value.is_following_with_id(request.user.pk)

        return False


class IsSentFollowRequestField(ReadOnlyField):
    def __init__(self, **kwargs):
        kwargs["source"] = "*"
        return super(IsSentFollowRequestField, self).__init__(**kwargs)

    def to_representation(self, value: "User"):
        request = self.context.get("request")

        if not request.user.is_anonymous:
            if request.user.pk == value.pk:
                return False
            return value.has_follow_request_with_id(request.user.pk)

        return False


class IsCameFollowRequestField(ReadOnlyField):
    def __init__(self, **kwargs):
        kwargs["source"] = "*"
        return super(IsCameFollowRequestField, self).__init__(**kwargs)

    def to_representation(self, value: "User"):
        request = self.context.get("request")

        if not request.user.is_anonymous:
            if request.user.pk == value.pk:
                return False
            return request.user.has_follow_request_with_id(value.pk)

        return False
