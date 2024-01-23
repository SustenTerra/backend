from app.controllers.base import BaseController
from app.models import CourseCategory
from app.repositories.course_category import CourseCategoryRepository
from app.schemas.course_category import (
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
