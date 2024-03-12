from typing import List

from fastapi import APIRouter, Depends

from app.course_category.controller import CourseCategoryController
from app.deps import get_course_category_controller
from app.course_category.schema import CourseCategoryView

course_categories = APIRouter()


@course_categories.get(
    "/course_categories",
    tags=["course_categories"],
    description="List all course_categories",
    response_model=List[CourseCategoryView],
)
def list_all_course_categories(
    controller: CourseCategoryController = Depends(
        get_course_category_controller
    ),
):
    return controller.get_all()
