from app.common.base.controller import BaseController
from app.learning.course_category.repository import CourseCategoryRepository
from app.learning.course_category.schema import (
    CourseCategoryCreate,
    CourseCategoryUpdate,
)
from app.models import CourseCategory


class CourseCategoryController(
    BaseController[
        CourseCategory,
        CourseCategoryRepository,
        CourseCategoryCreate,
        CourseCategoryUpdate,
    ]
):
    pass
