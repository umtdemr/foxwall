from django.db import IntegrityError

from rest_framework.exceptions import ValidationError

from follow.models import (
    FollowRequest
)


def create_follow_request(
    creator_id: int,
    target_id: int
):
    if creator_id == target_id:
        raise ValidationError(
            "You can't follow yourself"
        )

    try:
        FollowRequest.create_follow_request(
            creator_id,
            target_id
        )
    except IntegrityError:
        raise ValidationError(
            "You already follow this user"
        )


def delete_follow_request(
    creator_id: int,
    target_id: int
):
    FollowRequest.delete_follow_request(
        creator_id,
        target_id
    )
