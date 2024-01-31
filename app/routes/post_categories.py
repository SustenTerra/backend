from typing import List

from fastapi import APIRouter, Depends

from app.controllers.post_category import PostCategoryController
from app.deps import get_post_category_controller
from app.schemas.post_category import PostCategoryView

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
