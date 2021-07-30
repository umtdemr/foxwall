from django.db import models


class TimeInfoModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Created At",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated At",
        auto_now=True
    )

    class Meta:
        abstract = True
