from follow.utils import (
    get_users_followers_count,
    get_users_follows_count
)


def test_get_users_followers_count(follow_obj):
    assert get_users_followers_count(follow_obj.followed_user_id) == 1


def test_get_users_follows_count(follow_obj):
    assert get_users_follows_count(follow_obj.user_id) == 1