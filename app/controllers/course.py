from typing import Optional

from app.controllers.base import BaseController
from app.models import Course
from app.repositories.course import CourseRepository
from app.schemas.course import CourseCreate, CourseUpdate


class CourseController(
    BaseController[Course, CourseRepository, CourseCreate, CourseUpdate]
):
    def get_all(
        self,
        category_name: Optional[str] = None,
        search_term: Optional[str] = None,
    ) -> list[Course]:
        if category_name:
            return self.repository.get_all_by_category_name(category_name)

        if search_term:
            return self.repository.get_all_by_name_or_category_name(
                search_term
            )

        return super().get_all()
