from app.controllers.base import BaseController
from app.models import PostCategory
from app.repositories.post_category import PostCategoryRepository
from app.schemas.post_category import PostCategoryCreate, PostCategoryUpdate


class PostCategoryController(
    BaseController[
        PostCategory,
        PostCategoryRepository,
        PostCategoryCreate,
        PostCategoryUpdate,
    ]
):
    pass
