import re

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError


def email_not_taken_validator(email: str):
    User = get_user_model()
    if User.is_email_taken(email):
        raise ValidationError(_("Email address you entered exists"))


def username_not_taken_validator(username: str):
    User = get_user_model()
    if User.is_username_taken(username):
        raise ValidationError(_("Username you entered exists"))


def name_not_contain_k_validator(name: str):
    if "<" in name or ">" in name:
        raise ValidationError(_("Name should not contain < or >"))


def username_special_character_validator(username: str):
    if not re.match('^[a-zA-Z0-9_.]*$', username):
        raise ValidationError(_('Usernames has special characters'), )


def username_n_email_both_empty_validator(username: str, email: str):
    if email is None and username is None or email == "" and username == "":
        raise ValidationError(_("You should provide email and username"))


def user_email_exists(email: str):
    User = get_user_model()

    if User.objects.fitler(email=email).count() != 1:
        raise ValidationError(
            _("Email address is not valid for request")
        )
