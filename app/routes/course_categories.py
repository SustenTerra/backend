from fastapi import APIRouter, Depends

from app.controllers.course_category import CourseCategoryController
from app.deps import get_course_category_controller

course_categories = APIRouter()


@course_categories.get(
    "/course_categories",
    tags=["course_categories"],
    description="List all course_categories",
)
def list_all_course_categories(
    controller: CourseCategoryController = Depends(
        get_course_category_controller
    ),
):
    return controller.get_all()
