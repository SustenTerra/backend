from typing import Optional

from app.controllers.base import BaseController
from app.exceptions.user import UserNotAllowed
from app.models import Post
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostCreateWithImage, PostUpdate
from app.services.bucket_manager import BucketManager


class PostController(
    BaseController[
        Post,
        PostRepository,
        PostCreate,
        PostUpdate,
    ]
):
    def __init__(self, model_class: Post, repository: PostRepository):
        super().__init__(model_class, repository)
        self.bucket_manager = BucketManager()

    def _check_if_user_is_allowed(self, post_id, user_id) -> None:
        found_post = self.repository.get_by_id(post_id)

        if found_post and found_post.user_id != user_id:
            raise UserNotAllowed()

    def create(self, create: PostCreateWithImage) -> Post:
        image_key = self.bucket_manager.upload_file(create.image)

        body = PostCreate(
            image_key=image_key, **create.model_dump(exclude={"image"})
        )

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
    ) -> list[Post]:
        if category_name:
            return self.repository.get_by_category_name(category_name.strip())

        if search_term:
            return self.repository.get_by_search(search_term.strip())

        if user_id:
            return self.repository.get_by_user_id(user_id)

        return super().get_all()

    def update(self, id: int, update: PostUpdate, user_id: int) -> Post:
        self._check_if_user_is_allowed(id, user_id)

        return super().update(id, update)

    def delete(self, id: int, user_id: int) -> None:
        self._check_if_user_is_allowed(id, user_id)

        return super().delete(id)

    def get_top_5_viewed_posts(self):
        return self.repository.get_top_5_viewed_posts()
