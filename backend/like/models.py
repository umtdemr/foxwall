from typing import Optional

from django.db import models
from django.db.models import Q
from django.conf import settings

from core.abstract_models import TimeInfoModel
from post.models import Post


class Like(TimeInfoModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="likes",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(Post,
                             related_name="likes",
                             on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            'user',
            'post',
        )

    @classmethod
    def create_like(cls, user_id: int, post_id: int) -> "Like":
        like = Like.objects.create(
            user_id=user_id,
            post_id=post_id,
        )
        return like

    @classmethod
    def delete_lik(cls, user_id: int, post_id: int) -> "Like":
        return Like.objects.filter(user_id=user_id, post_id=post_id).delete()

    @classmethod
    def count_post_likes(cls,
                         post_id: int,
                         user_id: Optional[int] = None) -> int:
        count_query = Q(post_id=post_id, user__is_active=True)

        if user_id:
            count_query.add(Q(user_id=user_id), Q.AND)

        return cls.objects.filter(count_query).count()
