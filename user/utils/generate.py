import os
import re
from itertools import count

from django.core.files import File
from django.contrib.auth import get_user_model


PLACEHOLDER_DIR = "static_dev/placeholders/"


def generate_username(email: str) -> str:
    email_name = re.split("@", email)[0]

    for i in count(1):
        User = get_user_model()
        if User.objects.filter(
            username=email_name
        ).count() == 0:
            return email_name
        else:
            email_name = f"{email_name}{i}"


def generate_user_avatar():
    return get_image(
        PLACEHOLDER_DIR,
        "avatar.jpg"
    )


def generate_user_cover():
    return get_image(
        PLACEHOLDER_DIR,
        "cover.jpg"
    )


def get_image(image_dir, image_name):
    img_path = os.path.join(image_dir, image_name)
    return File(open(img_path, "rb"), name=image_name)
