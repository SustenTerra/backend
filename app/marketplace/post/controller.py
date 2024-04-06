from typing import Optional

from app.common.base.controller import BaseController
from app.common.user.exception import UserNotAllowed
from app.marketplace.post.exception import InvalidLocationException
from app.marketplace.post.repository import PostRepository
from app.marketplace.post.schema import (
    PostCreate,
    PostCreateWithImage,
    PostUpdate,
    PostUpdateWithImage,
)
from app.marketplace.post.utils import BR_STATES
from app.models import Post
from app.service.bucket_manager import BucketManager


class PostController(
    BaseController[
        Post,
        PostRepository,
        PostCreate,
        PostUpdate,
    ]
):
    def __init__(
        self,
        model_class: Post,
        repository: PostRepository,
        bucket_manager: BucketManager,
    ):
        super().__init__(model_class, repository)
        self.bucket_manager = bucket_manager

    def _check_if_user_is_allowed(self, post_id, user_id) -> None:
        found_post = self.repository.get_by_id(post_id)

        if found_post and found_post.user_id != user_id:
            raise UserNotAllowed()

    def __verify_location(self, location: str) -> None:
        if location.upper() not in BR_STATES:
            raise InvalidLocationException(location)

    def create(self, create: PostCreateWithImage) -> Post:
        self.__verify_location(create.location)

        image_key = self.bucket_manager.upload_file(create.image)

        body = PostCreate(image_key=image_key, **create.model_dump(exclude={"image"}))

        return super().create(body)

    def get_by_id(self, id: int) -> Post | None:
        found_post = self.repository.get_by_id(id)
        if found_post:
            super().update(id, PostUpdate(views=found_post.views + 1))

        return found_post

    def get_all(
        self,
        search_term: Optional[str],
        user_id: Optional[int],
        category_name: Optional[str],
        location: Optional[str],
    ) -> list[Post]:
        if location:
            if len(location) != 2 or not location.isalpha():
                raise InvalidLocationException(location=location)
            self.repository.location = location.strip()

        if category_name:
            return self.repository.get_by_category_name(category_name.strip())

        if search_term:
            return self.repository.get_by_search(search_term.strip())

        if user_id:
            return self.repository.get_by_user_id(user_id)

        return super().get_all()

    def update(self, id: int, update: PostUpdateWithImage, user_id: int) -> Post:
        self._check_if_user_is_allowed(id, user_id)

        if hasattr(update, "location") and update.location is not None:
            self.__verify_location(update.location)

        image_key = None
        if update.image:
            image_key = self.bucket_manager.upload_file(update.image)

        body = PostUpdate(image_key=image_key, **update.model_dump(exclude={"image"}))

        return super().update(id, body)

    def delete(self, id: int, user_id: int) -> None:
        self._check_if_user_is_allowed(id, user_id)

        return super().delete(id)

    def get_top_5_viewed_posts(self):
        return self.repository.get_top_5_viewed_posts()
