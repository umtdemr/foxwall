import pytest

from ..models import Like


pytestmark = pytest.mark.django_db


def test_create_like(valid_user, post_obj):
    like = Like.create_like(
        user_id=valid_user.id,
        post_id=post_obj.id
    )
    assert Like.objects.count() == 1
    assert like.user == valid_user
    assert like.post == post_obj


def test_delete_like(like_obj):
    assert Like.objects.count() == 1
    Like.delete_like(
        user_id=like_obj.user.id,
        post_id=like_obj.post.id
    )
    assert Like.objects.count() == 0


def test_count_like(like_obj, like_obj2):
    assert Like.count_post_likes(
        post_id=like_obj.post.id
    ) == 2
    assert Like.count_post_likes(
        post_id=like_obj2.post.id,
        user_id=like_obj2.user.id
    ) == 1
