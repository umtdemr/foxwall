from django.contrib import admin

from follow.models import Follow, FollowRequest

admin.site.register(Follow)
admin.site.register(FollowRequest)
