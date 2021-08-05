import os

from ..models import User, UserProfile


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
    t_cov = f"{tmpdir}/media/users/{user_profile.user.token}/{cover_file_name}"
    t_av = f"{tmpdir}/media/users/{user_profile.user.token}/{avatar_file_name}"
    assert os.path.exists(t_cov)
    assert os.path.exists(t_av)
    assert user_profile.cover.path == t_cov
    assert user_profile.avatar.path == t_av
