from follow.models import FollowRequest, Follow


def allow_follow_request(user_id: int, allowing_user_id: int):
    FollowRequest.delete_follow_request(
        creator_id=allowing_user_id,
        target_user_id=user_id
    )
    Follow.create_follow(
        user_id=allowing_user_id,
        followed_user_id=user_id
    )


def unfollow(
    user_id: int,
    unfollowing_user_id: int,
):
    Follow.delete_follow(
        user_id,
        unfollowing_user_id
    )
