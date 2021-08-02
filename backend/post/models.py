import uuid

from django.db import models
from django.conf import settings

from post import PostStatus, PostVisibility
from core.abstract_models import TimeInfoModel


class Post(TimeInfoModel):
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
    text = models.TextField()
    is_edited = models.BooleanField(default=False)
