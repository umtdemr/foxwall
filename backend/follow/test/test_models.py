import pytest

from django.db.utils import IntegrityError

from ..models import Follow, FollowRequest


@pytest.mark.django_db
def test_follow_request_create(valid_user, valid_user2):
    follow_request_obj = FollowRequest.create_follow_request(
        creator_id=valid_user.id,
        target_user_id=valid_user2.id
    )
    assert FollowRequest.objects.count() == 1
    assert follow_request_obj.creator == valid_user
    assert follow_request_obj.target_user == valid_user2
    try:
        FollowRequest.create_follow_request(
            creator_id=valid_user.id,
            target_user_id=valid_user2.id
        )
    except IntegrityError:
        assert 1


@pytest.mark.django_db
def test_follow_request_delete(follow_request_obj):
    assert FollowRequest.objects.count() == 1
    FollowRequest.delete_follow_request(
        creator_id=follow_request_obj.creator_id,
        target_user_id=follow_request_obj.target_user_id,
    )
    assert FollowRequest.objects.count() == 0


@pytest.mark.django_db
def test_follow_create(valid_user, valid_user2):
    follow_obj = Follow.create_follow(
        user_id=valid_user.id,
        followed_user_id=valid_user2.id
    )
    assert Follow.objects.count() == 1
    assert follow_obj.user == valid_user
    assert follow_obj.followed_user == valid_user2
    try:
        Follow.create_follow(
            user_id=valid_user.id,
            followed_user_id=valid_user2.id
        )
    except IntegrityError:
        assert 1


@pytest.mark.django_db
def test_follow_delete(follow_obj):
    assert Follow.objects.count() == 1
    Follow.delete_follow(
        user_id=follow_obj.user_id,
        followed_user_id=follow_obj.followed_user_id,
    )
    assert Follow.objects.count() == 0
