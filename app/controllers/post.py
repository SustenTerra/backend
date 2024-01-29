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
        img_key = self.bucket_manager.upload_file(create.image)
        create.image_url = self.bucket_manager.get_presigned_url(img_key)

        return super().create(PostCreate(**create.model_dump()))

    def update(self, id: int, update: PostUpdate, user_id: int) -> Post:
        self._check_if_user_is_allowed(id, user_id)

        return super().update(id, update)

    def delete(self, id: int, user_id: int) -> None:
        self._check_if_user_is_allowed(id, user_id)

        return super().delete(id)
