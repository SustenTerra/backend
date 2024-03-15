from typing import List

from fastapi import APIRouter, Depends

from app.post_category.controller import PostCategoryController
from app.post_category.deps import get_post_category_controller
from app.post_category.schema import PostCategoryView

post_categories = APIRouter()


@post_categories.get(
    "/post_categories",
    tags=["post_categories"],
    description="List all post_categories",
    response_model=List[PostCategoryView],
)
def list_all_post_categories(
    controller: PostCategoryController = Depends(get_post_category_controller),
):
    return controller.get_all()
