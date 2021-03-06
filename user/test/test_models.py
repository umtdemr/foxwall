import os

import pytest

from ..models import User, UserProfile

pytestmark = pytest.mark.django_db


def test_user_can_create(valid_user):
    count = User.objects.count()
    assert count == 1


def test_user_profile_can_create(valid_user_profile):
    count = UserProfile.objects.count()
    assert count == 1


def test_user_profile_media_path(tmpdir, valid_user_profile):
    user_profile = valid_user_profile
    cover_file_name = os.path.basename(user_profile.cover.name)
    avatar_file_name = os.path.basename(user_profile.avatar.name)
    t_cov = f"{tmpdir}/media/users/{user_profile.user.sec_token}" \
            f"/{cover_file_name}"
    t_av = f"{tmpdir}/media/users/{user_profile.user.sec_token}" \
           f"/{avatar_file_name}"
    assert os.path.exists(t_cov)
    assert os.path.exists(t_av)
    assert user_profile.cover.path == t_cov
    assert user_profile.avatar.path == t_av


@pytest.mark.parametrize("username, email, password, is_super, error", [
    ("mediumgoal", "mediumgoal@gmail.com", "deneme", False, False),
    ("mediumgoal2", "mediumgoals@gmail.com", "deneme", True, False),
    ("mediumgoalx", None, "deneme", False, True),
    (None, "mediq@gmail.com", "deneme", False, True),
    ("mediumgoal", "mediq@gmail.com", None, False, False),
])
def test_user_manager(username, email, password, is_super, error):
    try:
        if not is_super:
            user = User.objects.create_user(
                email=email,
                password=password,
                username=username,
            )
        else:
            user = User.objects.create_superuser(email, password, username)
        assert user.username == username
        assert user.email == email
        if password is None:
            assert not user.check_password(password)
    except ValueError:
        if error:
            assert 1
        else:
            assert 0
