import uuid

from django.db import models
from django.conf import settings

from mptt.models import MPTTModel
from mptt.managers import TreeManager

from post import PostStatus, PostVisibility
from core.abstract_models import TimeInfoModel


class PostQuerySet(models.QuerySet):
    pass


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

    objects = PostQuerySet.as_manager()
    tree_objects = TreeManager()

    def __str__(self) -> str:
        return str(self.user)

    def __repr__(self) -> str:
        return f"<Post {self.user!r}>"
