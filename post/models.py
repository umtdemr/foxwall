import uuid
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Count, Value
from django.db.models.functions import Coalesce
from django.conf import settings

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from post import PostStatus, PostVisibility
from post.utils import post_image_upload_directory
from core.abstract_models import TimeInfoModel


if TYPE_CHECKING:
    from user.models import User


class PostQuerySet(models.QuerySet):
    def get_timeline_posts(self, user: "User"):
        user_ids = user.get_follows().values_list("followed_user__id", flat=True)
        try:
            user_ids = list(user_ids)
            #  Add current user's posts to timeline posts
            user_ids.append(user.pk)
        except Exception:
            user_ids = user.get_follows().values("followed_user__id")

        return self.filter(
            user_id__in=user_ids,
            status=PostStatus.PUBLISHED,
            visibility=PostVisibility.VISIBLE,
        ).annotate(
            num_likes=Coalesce(Count("likes"), Value(0))
        ).order_by("-created_at")

    def get_user_posts(self, user_id: int):
        return self.filter(
            user_id=user_id,
            status=PostStatus.PUBLISHED,
            visibility=PostVisibility.VISIBLE,
        ).annotate(
            num_likes=Coalesce(Count("likes"), Value(0))
        ).order_by("-created_at")

    def get_user_posts_with_username(self, username: str):
        return self.filter(
            user__username=username,
            status=PostStatus.PUBLISHED,
            visibility=PostVisibility.VISIBLE,
        ).annotate(
            num_likes=Coalesce(Count("likes"), Value(0))
        ).order_by("-created_at")


class Post(MPTTModel, TimeInfoModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="posts",
                             on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=True,
                            db_index=True)
    status = models.CharField(
        max_length=12,
        choices=PostStatus.CHOICES,
        default=PostStatus.DRAFT,
    )
    visibility = models.CharField(
        max_length=12,
        choices=PostVisibility.CHOICES,
        default=PostVisibility.VISIBLE,
    )
    text = models.TextField(blank=True, null=True)
    is_edited = models.BooleanField(default=False)
    parent = models.ForeignKey("self",
                               blank=True,
                               null=True,
                               related_name="replies",
                               on_delete=models.SET_NULL)

    active = PostQuerySet.as_manager()
    tree_objects = TreeManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.user)

    def __repr__(self) -> str:
        return f"<Post {self.user!r}>"


class PostImage(TimeInfoModel):
    post = models.ForeignKey(
        Post,
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = ProcessedImageField(
        processors=[ResizeToFit(width=700, upscale=False)],
        upload_to=post_image_upload_directory,
    )

    def __str__(self) -> str:
        return str(self.post)
