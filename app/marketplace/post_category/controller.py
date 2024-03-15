from app.common.base.controller import BaseController
from app.marketplace.post_category.repository import PostCategoryRepository
from app.marketplace.post_category.schema import (
    PostCategoryCreate,
    PostCategoryUpdate,
)
from app.models import PostCategory


class PostCategoryController(
    BaseController[
        PostCategory,
        PostCategoryRepository,
        PostCategoryCreate,
        PostCategoryUpdate,
    ]
):
    pass
