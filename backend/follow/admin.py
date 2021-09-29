from django.contrib import admin

from follow.models import Follow, FollowRequest


@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ("creator", "target_user", )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user", )
