from app.controllers.base import BaseController
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
    def create(self, create: PostCreate, user_id: int) -> Post:
        create.user_id = user_id
        return super().create(create)
