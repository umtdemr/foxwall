from typing import TYPE_CHECKING

from core.utils.files import generate_new_filename

if TYPE_CHECKING:
    from user.models import UserProfile, User


def create_username_with_mail():
    pass


def upload_to_user_directory(
    user_profile: "UserProfile",
    filename: str,
) -> str:
    user = user_profile.user
    return _upload_to_user_directory(user, filename)


def _upload_to_user_directory(user: "User", filename: str) -> str:
    generated_filename = generate_new_filename(filename)
    path = f"users/{user.token}/{generated_filename}"
    return path
