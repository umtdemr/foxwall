from django.db import models
from django.conf import settings

from core.abstract_models import TimeInfoModel


class FollowRequest(TimeInfoModel):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_follow_requests",
        on_delete=models.CASCADE,
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="coming_follow_requests",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            "creator",
            "target_user",
        )
        indexes = [
            models.Index(
                fields=["creator", "target_user"],
                name="indexed_creator_n_target",
            )
        ]

    @classmethod
    def create_follow_request(cls, creator_id, target_user_id):
        follow_request = FollowRequest.objects.create(
            creator_id=creator_id, target_user_id=target_user_id)
        return follow_request

    @classmethod
    def delete_follow_request(cls, creator_id, target_user_id):
        return FollowRequest.objects.filter(
            creator_id=creator_id, target_user_id=target_user_id).delete()


class Follow(TimeInfoModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="follows",
        on_delete=models.CASCADE,
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="followers",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )
        indexes = [
            models.Index(fields=["user", "followed_user"],
                         name="indexed_user_n_followed_user")
        ]

    @classmethod
    def create_follow(cls, user_id, followed_user_id):
        follow = Follow.objects.create(user_id=user_id,
                                       followed_user_id=followed_user_id)
        return follow

    @classmethod
    def delete_follow(cls, user_id, followed_user_id):
        return Follow.objects.filter(
            user_id=user_id, followed_user_id=followed_user_id).delete()
