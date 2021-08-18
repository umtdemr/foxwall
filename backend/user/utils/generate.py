import os

from django.core.files import File


PLACEHOLDER_DIR = "static_dev/placeholders/"


def generate_user_avatar():
    return get_image(
        PLACEHOLDER_DIR,
        "cover.jpg"
    )


def generate_user_cover():
    return get_image(
        PLACEHOLDER_DIR,
        "avatar.jpg"
    )


def get_image(image_dir, image_name):
    img_path = os.path.join(image_dir, image_name)
    return File(open(img_path, "rb"), name=image_name)
