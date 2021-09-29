from django.utils.translation import ugettext_lazy as _

from rest_framework.permissions import BasePermission


class PostIsOwner(BasePermission):
    message = _("You are not owner this post")

    def has_object_permission(self, request, view, obj):

        return obj.user == request.user
