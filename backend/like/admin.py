from django.contrib import admin

from like.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    search_fields = (
        "user_id",
        "user__name",
    )
    list_display = ["user", "post", "created_at"]
