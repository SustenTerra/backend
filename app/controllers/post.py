from app.controllers.base import BaseController
from app.exceptions.user import UserNotAllowed
from app.models import Post
from app.repositories.post import PostRepository
from app.schemas.post import (
    PostCreate,
    PostUpdate,
)


class PostController(
    BaseController[
        Post,
        PostRepository,
        PostCreate,
        PostUpdate,
    ]
):
    def check_if_user_is_allowed(self, post_id, user_id) -> None:
        found_post = self.repository.get_by_id(post_id)

        if found_post and found_post.user_id != user_id:
            raise UserNotAllowed()

    def create(self, create: PostCreate, user_id: int) -> Post:
        create.user_id = user_id
        return super().create(create)

    def update(self, id: int, update: PostUpdate, user_id: int) -> Post:
        self.check_if_user_is_allowed(id, user_id)

        return super().update(id, update)

    def delete(self, id: int, user_id: int) -> None:
        self.check_if_user_is_allowed(id, user_id)

        return super().delete(id)
