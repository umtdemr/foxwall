from typing import Any, Dict, TYPE_CHECKING

from core.utils.files import generate_new_filename
from user.views.authenticated.serializers import UserSerializer

if TYPE_CHECKING:
    from user.models import UserProfile, User


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


def get_user_dict_data(user: "User") -> Dict[str, Any]:
    user_profile = user.get_profile()
    return {
        "username": user.username,
        "email": user.email,
        "name": user_profile.name,
        "bio": user_profile.bio,
        "avatar": user_profile.avatar,
        "cover": user_profile.cover,
        "is_hidden": user_profile.is_hidden,
        "is_celebrity": user_profile.is_celebrity,
    }


def get_user_data_with_serializer(user: "User") -> UserSerializer:
    data = get_user_dict_data(user)
    return UserSerializer(data=data)
