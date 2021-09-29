import pytest
import tempfile

from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings  # noqa

from PIL import Image

from user.models import User, UserProfile
from post.models import PostStatus
from post.models import Post, PostImage
from like.models import Like
from follow.models import FollowRequest, Follow


@pytest.fixture
def image():
    img_data = BytesIO()
    image = Image.new("RGB", size=(1, 1))
    image.save(img_data, format="JPEG")
    return SimpleUploadedFile("product.jpg", img_data.getvalue())


@pytest.fixture
def media_root(tmpdir, settings):  # noqa
    settings.MEDIA_ROOT = str(tmpdir.mkdir("media"))


@pytest.fixture
def valid_user(db):
    user = User.objects.create_user(
        email="deneme@w.com",
        password="password",
        username="mediumgoal",
    )
    return user


@pytest.fixture
def valid_user2(db):
    user = User.objects.create_user(
        email="deneme@w.scom",
        password="passwsord",
        username="mediumgoals",
    )
    return user


@pytest.fixture
def valid_user_profile(db, valid_user, image, media_root):
    return UserProfile.objects.create(user=valid_user,
                                      name="ümit",
                                      avatar=image,
                                      cover=image,
                                      bio="some text")


@pytest.fixture
def post_obj(db, valid_user):
    post = Post.objects.create(user=valid_user,
                               status=PostStatus.PUBLISHED,
                               text="Hi this is an example post")
    return post


@pytest.fixture
def post_img_obj(db, post_obj, image, media_root):
    return PostImage.objects.create(post=post_obj, image=image)


@pytest.fixture
def like_obj(db, valid_user, post_obj):
    return Like.create_like(user_id=valid_user.id, post_id=post_obj.id)


@pytest.fixture
def like_obj2(db, valid_user2, post_obj):
    return Like.create_like(user_id=valid_user2.id, post_id=post_obj.id)


@pytest.fixture
def follow_request_obj(db, valid_user, valid_user2):
    return FollowRequest.objects.create(creator_id=valid_user.id,
                                        target_user_id=valid_user2.id)


@pytest.fixture
def follow_request_obj2(db, valid_user, valid_user2):
    return FollowRequest.objects.create(  # pragma: no cover
        creator_id=valid_user2.id,
        target_user_id=valid_user.id)


@pytest.fixture
def follow_obj(db, valid_user, valid_user2):
    return Follow.objects.create(  # pragma: no cover
        user_id=valid_user2.id,
        followed_user_id=valid_user.id)


@pytest.fixture
def follow_obj2(db, valid_user, valid_user2):
    return Follow.objects.create(  # pragma: no cover
        user_id=valid_user.id,
        followed_user_id=valid_user2.id)


@pytest.fixture
def user_avatar():
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file


@pytest.fixture
def user_cover():
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file)
    tmp_file.seek(0)
    return tmp_file


@pytest.fixture
def image_obj3():
    img_data = BytesIO()
    image = Image.new("RGB", size=(100, 100))
    image.save(img_data, format="JPEG")
    return SimpleUploadedFile("products.jpg", img_data.getvalue())
