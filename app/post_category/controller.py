from app.controllers.base import BaseController
from app.models import PostCategory
from app.post_category.repository import PostCategoryRepository
from app.post_category.schema import PostCategoryCreate, PostCategoryUpdate


class PostCategoryController(
    BaseController[
        PostCategory,
        PostCategoryRepository,
        PostCategoryCreate,
        PostCategoryUpdate,
    ]
):
    pass
