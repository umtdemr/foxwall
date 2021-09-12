from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import ValidationError


def text_or_image_must_required(text, image):
    if not text and not image:
        raise ValidationError(
            _("Image or Text is required")
        )
