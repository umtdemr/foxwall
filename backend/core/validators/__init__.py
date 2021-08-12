import re

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


def name_not_contain_k_validator(name: str):
    if "<" or ">" in name:
        return ValidationError(
            _("Name should not contain < or >")
        )


def username_special_character_validator(username: str):
    if not re.match('^[a-zA-Z0-9_.]*$', username):
        raise ValidationError(
            _('Usernames has special characters'),
        )
