from typing import TYPE_CHECKING

from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError


if TYPE_CHECKING:
    from rest_framework.request import Request


def required_query_param(query: str, request: "Request"):
    if not request.query_params.get(query):
        raise ValidationError(
            _(f"Missing required query param for: {query}")
        )
