from rest_framework.pagination import LimitOffsetPagination


class PostPagination(LimitOffsetPagination):
    page_size = 25
    default_limit = 25
