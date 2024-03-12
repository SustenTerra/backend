from app.controllers.base import BaseController
from app.models import CourseCategory
from app.course_category.repository import CourseCategoryRepository
from app.course_category.schema import (
    CourseCategoryCreate,
    CourseCategoryUpdate,
)


class CourseCategoryController(
    BaseController[
        CourseCategory,
        CourseCategoryRepository,
        CourseCategoryCreate,
        CourseCategoryUpdate,
    ]
):
    pass
