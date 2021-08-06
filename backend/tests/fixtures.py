from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from PIL import Image
import pytest

from user.models import User, UserProfile
from post.models import PostStatus
from post.models import Post, PostImage
from like.models import Like


@pytest.fixture
def image():
    img_data = BytesIO()
    image = Image.new("RGB", size=(1, 1))
    image.save(img_data, format="JPEG")
    return SimpleUploadedFile("product.jpg", img_data.getvalue())


@pytest.fixture
def media_root(tmpdir, settings):
    settings.MEDIA_ROOT = str(tmpdir.mkdir("media"))


@pytest.fixture
def valid_user(db):
    user = User.objects.create(
        username="mediumgoal",
        email="deneme@w.com",
        password="password"
    )
    return user


@pytest.fixture
def valid_user2(db):
    user = User.objects.create(
        username="mediumgoals",
        email="deneme@w.scom",
        password="passwsord"
    )
    return user


@pytest.fixture
def valid_user_profile(db, valid_user, image, media_root):
    return UserProfile.objects.create(
        user=valid_user,
        avatar=image,
        cover=image,
        bio="some text"
    )


@pytest.fixture
def post_obj(db, valid_user):
    post = Post.objects.create(
        user=valid_user,
        status=PostStatus.PUBLISHED,
        text="Hi this is an example post"
    )
    return post


@pytest.fixture
def post_img_obj(db, post_obj, image, media_root):
    return PostImage.objects.create(
        post=post_obj,
        image=image
    )


@pytest.fixture
def like_obj(db, valid_user, post_obj):
    return Like.create_like(
        user_id=valid_user.id,
        post_id=post_obj.id
    )


@pytest.fixture
def like_obj2(db, valid_user2, post_obj):
    return Like.create_like(
        user_id=valid_user2.id,
        post_id=post_obj.id
    )
