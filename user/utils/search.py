from django.db.models import Q

from user.models import User


def search_user(q: str):
    query = User.objects.filter(
        Q(username__icontains=q.lower()) |
        Q(email__icontains=q.lower()) |
        Q(profile__name__icontains=q.lower()) |
        Q(profile__bio__icontains=q.lower())
    )
    return query, query.count()
