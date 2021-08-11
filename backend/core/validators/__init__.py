from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError

from user.models import User


def email_not_taken_validator(email: str):
    if User.is_email_taken(email):
        return ValidationError(
            _("Email address you entered exists")
        )


def username_not_taken_validator(username: str):
    if User.is_username_taken(username):
        return ValidationError(
            _("Username you entered exists")
        )
