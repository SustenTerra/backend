import pytest
from fastapi import UploadFile
from io import BytesIO
from unittest.mock import MagicMock

from app.models import Post
from app.marketplace.post.repository import PostRepository
from app.marketplace.post.schema import PostCreateWithImage
from app.service.bucket_manager import BucketManager
from app.marketplace.post.controller import PostController
from app.marketplace.post.exception import InvalidLocationException


class TestPostController:
    @pytest.fixture
    def setup(self, db_session, make_user):
        bucket_manager_mock = MagicMock(spec=BucketManager)
        bucket_manager_mock.upload_file.return_value = "path/to/image.jpg"

        post_repository = PostRepository(Post, db_session)
        post_controller = PostController(Post, post_repository)
        post_controller.bucket_manager = bucket_manager_mock

        user_password = "teste12345"
        user = make_user(
            email="user@example.com",
            password=user_password,
        )

        db_session.add(user)
        db_session.commit()

        self.common_title = "Test Post"
        self.common_description = "Test Description"
        self.common_price = 100
        self.common_post_type = "sell"
        self.common_location = "SP"
        self.common_category_id = 1

        return post_controller, user, bucket_manager_mock

    def test_create_post_successfully(self, setup):
        post_controller, user, bucket_manager_mock = setup

        fake_file = BytesIO(b"fake image data")
        fake_file.name = "test.jpg"

        upload_file = UploadFile(filename=fake_file.name, file=fake_file)

        post_data = PostCreateWithImage(
            title=self.common_title,
            image=upload_file,
            description=self.common_description,
            price=self.common_price,
            post_type=self.common_post_type,
            location=self.common_location,
            category_id=self.common_category_id,
            user_id=user.id,
        )

        created_post = post_controller.create(post_data)

        assert created_post is not None
        assert created_post.title == self.common_title
        assert created_post.description == post_data.description
        assert created_post.price == post_data.price
        assert created_post.post_type == post_data.post_type
        assert created_post.location == post_data.location
        assert created_post.category_id == post_data.category_id

        post_controller.bucket_manager.upload_file.assert_called_once()

    def test_create_post_with_invalid_state(self, setup):
        post_controller, user, bucket_manager_mock = setup

        fake_file = BytesIO(b"fake image data")
        fake_file.name = "test.jpg"
        upload_file = UploadFile(filename=fake_file.name, file=fake_file)

        invalid_state = "XX"
        post_data = PostCreateWithImage(
            title=self.common_title,
            image=upload_file,
            description=self.common_description,
            price=self.common_price,
            post_type=self.common_post_type,
            location=invalid_state,
            category_id=self.common_category_id,
            user_id=user.id,
        )
        with pytest.raises(InvalidLocationException):
            post_controller.create(post_data)

        bucket_manager_mock.upload_file.assert_not_called()