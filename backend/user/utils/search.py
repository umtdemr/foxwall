from django.db.models import Q

from user.models import User


def search_user(q: str):
    query = User.objects.filter(
        Q(username__icontains=q) |
        Q(email__icontains=q) |
        Q(profile__name__icontains=q)
    )
    return query, query.count()
